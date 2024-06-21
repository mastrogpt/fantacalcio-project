import uuid
from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import delete
from models.base import Base

from datetime import datetime


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
        else:
            return {"body": Article.get_all_articles(session)}

    def delete_handler(session, args):
        if 'id' in args:
            return {"body": Article.delete_by_id(session, args['id'])}
        else:
            return {"body": Article.delete_all(session)}

    
    def get_all_articles(session):
        try:
            articles = session.query(Article).all()
            return [article.to_dict() for article in articles]
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
