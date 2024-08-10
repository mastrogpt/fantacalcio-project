import uuid
from sqlalchemy.sql import delete
from models.base import Base
from sqlalchemy import desc
from sqlalchemy import Column, Integer, String,Text, ARRAY, DateTime, Boolean, Date, insert, UniqueConstraint, delete
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import aliased
from sqlalchemy import func
from sqlalchemy import desc
import uuid
from datetime import datetime
import json
from sqlalchemy import func, literal_column, table, column
from sqlalchemy.orm import aliased

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False)
    creation_date = Column(DateTime, default=datetime.now)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255))
    content = Column(Text, nullable=False)
    tag = Column(ARRAY(String(100)))
    category = Column(ARRAY(String(100)))
    author = Column(String(100))

    def __init__(self, uuid, title, subtitle, content, author, tag=None, category=None):
        self.uuid = uuid
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.author = author

        self.tag = tag
        self.category = category

    def __repr__(self):
        return f"<Article(uuid={self.uuid}, title='{self.title}', subtitle='{self.subtitle}', content='{self.content}', tag='{self.tag}', category='{self.category}', author='{self.author}')>"
    
    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
        
      
        if query_type == "delete":
            return Article.delete_handler(session, args)
        elif query_type == "new":
            if 'articles' in args:
                success = Article.save_articles(session, args['articles'])
    
                if success:
                    return {"statusCode": 200, "body": "Articles saved successfully"}
                else:
                    return {"statusCode": 500, "body": "Failed to save articles"}
            else:
                return {"statusCode": 400, "body": "No articles provided in the payload"}

        else:
            return Article.get_handler(session, args)
    
    def get_handler(session, args):
        if 'id' in args:
            article = Article.get_article_by_id(session, args['id'])
            return {"body": article if article else "Article not found"}
        elif 'last' in args:
            return {"body": Article.get_last_articles(session, args)}
        else:
            return {"body": Article.get_all_articles(session, args)}

    def delete_handler(session, args):
        if 'id' in args:
            return {"body": Article.delete_by_id(session, args['id'])}
        else:
            return {"body": Article.delete_all(session)}

    
    def get_all_articles(session, args):
        try:
            limit = args.get('limit', None)
            if limit:
                articles = session.query(Article).order_by(desc(Article.creation_date)).limit(limit)
            else :
                articles = session.query(Article).order_by(desc(Article.creation_date)).all()
            return [article.to_dict() for article in articles]
        except Exception as e:
            print("Error during articles loading:", e)
            return []
        finally:
            session.close()
            
    def get_last_articles(session, args):
        try:
            tag_search = args.get('tag', None)
            
            query = session.query(Article).order_by(desc(Article.creation_date))
            
            if tag_search:
                search_pattern = f"%{tag_search.lower()}%"
                
                subquery = (
                    session.query(
                        Article.id.label('article_id'), 
                        func.unnest(Article.tag).label('tag')
                    ).subquery()
                )
                
                tags_alias = aliased(subquery)
                
                # Filter articles based on the unnest subquery
                query = query.join(tags_alias, Article.id == tags_alias.c.article_id).filter(func.lower(tags_alias.c.tag).like(search_pattern))
            
            limit = 5 if tag_search else 10
            results = query.limit(limit).all()
            
            print("Articles fetched:", results)
            
            articles = [{'content': r.content} for r in results]
            
            return articles
        except Exception as e:
            print("Error during articles loading:", e)
            return []
        finally:
            session.close()


    def delete_all(session):
        try:
            session.execute(delete(Article))
            session.commit()
            return "All articles deleted"
        except Exception as e:
            print("Error while deleting articles:", e)
            session.rollback()
            return "Error while deleting articles"
        finally:
            session.close()

    def delete_by_id(session, article_id):
        try:
            article = session.query(Article).get(article_id)
            if article:
                session.delete(article)
                session.commit()
                return f"Article {article_id} deleted"
            else:
                return "Article not found"
        except Exception as e:
            print("Error while deleting article:", e)
            session.rollback()
            return "Error while deleting article"
        finally:
            session.close()

    def save_articles(session, articles):
        try:
            for article in articles:
                new_article = Article(
                    uuid=str(uuid.uuid4()),
                    title=article['title'],
                    subtitle=article['subtitle'],
                    content=article['content'],
                    author = article['author'],

                    tag=article.get('tag', []),
                    category=article.get('category', [])
                )
                session.add(new_article)
            session.commit()
            return True
        except Exception as e:
            print("Error during articles saving:", e)
            session.rollback()
            return False
        finally:
            session.close()

    def get_article_by_id(session, article_id):
        try:
            article = session.query(Article).get(article_id)
            return article.to_dict() if article else None
        except Exception as e:
            print("Error during article loading:", e)
            return None
        finally:
            session.close()

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'creation_date': self.creation_date.isoformat(),
            'title': self.title,
            'subtitle': self.subtitle,
            'content': self.content,
            'tag': self.tag,
            'category': self.category,
            'author': self.author
        }
