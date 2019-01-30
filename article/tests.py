from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from article.models import HomeArticle, UserArticle
from tests.utils import create_mock_user, get_test_graphql_client, get_query_context


# TODO(keshen): Add mutation test.
class HomeArticleTest(TestCase):
    TEST_MOCK_USERNAME = "TESTING-USERNAME"
    TEST_MOCK_PASSWORD = "TESTING-PASSWORD"
    TEST_ARTICLE_TITLE = "Romeo and Juliet"
    TEST_ARTILE_CONTENT = "deerC nissassA"
    TEST_ARTICLE_PREVIEW = "Odyssey"
    TEST_EXECUTE_QUERY = '''
        query getHomeArticle( $pk: ID ){
            homeArticle( pk: $pk ){
                title
                content
                author{
                    username
                }
                preview
            }
        }
    '''

    def setUp(self):
        self.mock_usr = create_mock_user(self.TEST_MOCK_USERNAME, self.TEST_MOCK_PASSWORD)
        self.test_article = HomeArticle.objects.create(
            title=self.TEST_ARTICLE_TITLE,
            author=self.mock_usr,
            content=self.TEST_ARTILE_CONTENT,
            preview=self.TEST_ARTICLE_PREVIEW
        )

    @staticmethod
    def get_response_result(response):
        return response.get('data').get('homeArticle')

    def test_query_home_article(self):
        client = get_test_graphql_client()
        response = client.execute(
            self.TEST_EXECUTE_QUERY,
            variables={
                'pk': self.test_article.pk
            }
        )
        assert HomeArticleTest.get_response_result(response) == {
            'title': self.TEST_ARTICLE_TITLE,
            'content': self.TEST_ARTILE_CONTENT,
            'author': {
                'username': self.TEST_MOCK_USERNAME
            },
            'preview': self.TEST_ARTICLE_PREVIEW
        }

    def test_query_disable_article(self):
        context = get_query_context()
        context.user = self.mock_usr
        self.test_article.disable = True
        self.test_article.save()
        client = get_test_graphql_client()
        response = client.execute(
            self.TEST_EXECUTE_QUERY,
            variables={
                'pk': self.test_article.pk
            },
            context_value=context
        )
        assert HomeArticleTest.get_response_result(response) is None

    def test_query_disable_article_with_permission_allowed(self):
        perm = Permission.objects.get(content_type=ContentType.objects.get_for_model(HomeArticle),
                                      codename="view_homearticle")
        self.mock_usr.user_permissions.add(perm)
        self.mock_usr.save()
        client = get_test_graphql_client()
        response = client.execute(
            self.TEST_EXECUTE_QUERY,
            variables={
                'pk': self.test_article.pk
            }
        )
        assert HomeArticleTest.get_response_result(response) == {
            'title': self.TEST_ARTICLE_TITLE,
            'content': self.TEST_ARTILE_CONTENT,
            'author': {
                'username': self.TEST_MOCK_USERNAME
            },
            'preview': self.TEST_ARTICLE_PREVIEW
        }


# TODO(keshen): Add mutation test.
class UserArticleTest(TestCase):
    TEST_MOCK_USERNAME = "TESTING-USERNAME"
    TEST_MOCK_PASSWORD = "TESTING-PASSWORD"
    TEST_ARTICLE_TITLE = "Juliet and Romeo"
    TEST_ARTILE_CONTENT = "nissassA deerC"
    TEST_ARTICLE_PREVIEW = "Origin"
    TEST_EXECUTE_QUERY = '''
        query getUserArticle( $pk: ID ){
            userArticle( pk: $pk ){
                title
                content
                author{
                    username
                }
            }
        }
    '''

    def setUp(self):
        self.mock_usr = create_mock_user(self.TEST_MOCK_USERNAME, self.TEST_MOCK_PASSWORD)
        self.test_article = UserArticle.objects.create(
            title=self.TEST_ARTICLE_TITLE,
            author=self.mock_usr,
            content=self.TEST_ARTILE_CONTENT,
        )

    @staticmethod
    def get_response_result(response):
        return response.get('data').get('userArticle')

    def test_query_user_article(self):
        client = get_test_graphql_client()
        response = client.execute(
            self.TEST_EXECUTE_QUERY,
            variables={
                'pk': self.test_article.pk
            }
        )
        assert UserArticleTest.get_response_result(response) == {
            'title': self.TEST_ARTICLE_TITLE,
            'content': self.TEST_ARTILE_CONTENT,
            'author': {
                'username': self.TEST_MOCK_USERNAME
            }
        }

    def test_query_disable_article(self):
        context = get_query_context()
        context.user = self.mock_usr
        self.test_article.disable = True
        self.test_article.save()
        client = get_test_graphql_client()
        response = client.execute(
            self.TEST_EXECUTE_QUERY,
            variables={
                'pk': self.test_article.pk
            },
            context_value=context
        )
        assert UserArticleTest.get_response_result(response) is None

    def test_query_disable_article_with_permission_allowed(self):
        perm = Permission.objects.get(content_type=ContentType.objects.get_for_model(UserArticle),
                                      codename="view_userarticle")
        self.mock_usr.user_permissions.add(perm)
        self.mock_usr.save()
        client = get_test_graphql_client()
        response = client.execute(
            self.TEST_EXECUTE_QUERY,
            variables={
                'pk': self.test_article.pk
            }
        )
        assert UserArticleTest.get_response_result(response) == {
            'title': self.TEST_ARTICLE_TITLE,
            'content': self.TEST_ARTILE_CONTENT,
            'author': {
                'username': self.TEST_MOCK_USERNAME
            }
        }


class UpdateArticleTest(TestCase):
    TEST_MOCK_USERNAME = "TESTING-USERNAME"
    TEST_MOCK_PASSWORD = "TESTING-PASSWORD"
    TEST_ARTICLE_TITLE = "Juliet and Romeo"
    TEST_ARTILE_CONTENT = "nissassA deerC"
    TEST_ARTICLE_PREVIEW = "Origin"
    TEST_CREATE_USER_ARTICLE = '''
        mutation createUserArticle(){
            
        }
    '''
    TEST_QUERY_USER_ARTICLE = '''
        query getUserArticle( $pk: ID ){
            userArticle( pk: $pk ){
                title
                content
                author{
                    username
                }
            }
        }
    '''

    def test_create_and_update_article(self):
        pass
