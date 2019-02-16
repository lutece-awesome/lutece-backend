from annoying.functions import get_object_or_None
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from article.models import HomeArticle, UserArticle, ArticleComment
from tests.utils import create_mock_user, get_test_graphql_client, get_query_context


# TODO(keshen): Add mutation test.
class HomeArticleTest(TestCase):
    TEST_MOCK_USERNAME = "TESTING-USERNAME"
    TEST_MOCK_PASSWORD = "TESTING-PASSWORD"
    TEST_ARTICLE_TITLE = "Romeo and Juliet"
    TEST_ARTICLE_CONTENT = "deerC nissassA"
    TEST_ARTICLE_PREVIEW = "Odyssey"
    TEST_EXECUTE_QUERY = '''
        query GetHomeArticle( $slug: ID ){
            homeArticle( slug: $slug ){
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
            content=self.TEST_ARTICLE_CONTENT,
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
                'slug': self.test_article.slug
            }
        )
        assert HomeArticleTest.get_response_result(response) == {
            'title': self.TEST_ARTICLE_TITLE,
            'content': self.TEST_ARTICLE_CONTENT,
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
                'slug': self.test_article.slug
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
                'slug': self.test_article.slug
            }
        )
        assert HomeArticleTest.get_response_result(response) == {
            'title': self.TEST_ARTICLE_TITLE,
            'content': self.TEST_ARTICLE_CONTENT,
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
    TEST_ARTICLE_CONTENT = "nissassA deerC"
    TEST_ARTICLE_PREVIEW = "Origin"
    TEST_EXECUTE_QUERY = '''
        query GetUserArticle( $pk: ID ){
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
            content=self.TEST_ARTICLE_CONTENT,
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
            'content': self.TEST_ARTICLE_CONTENT,
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
            'content': self.TEST_ARTICLE_CONTENT,
            'author': {
                'username': self.TEST_MOCK_USERNAME
            }
        }


class UpdateArticleTest(TestCase):
    TEST_MOCK_USERNAME = "TESTING-USERNAME"
    TEST_MOCK_PASSWORD = "TESTING-PASSWORD"
    TEST_ARTICLE_TITLE = "Juliet and Romeo"
    TEST_ARTICLE_CONTENT = "nissassA deerC"
    TEST_ARTICLE_PREVIEW = "Origin"
    TEST_CREATE_USER_ARTICLE = '''
        mutation CreateUserArticle( $title: String! , $content: String! ){
            createUserArticle( title: $title, content: $content ){
                pk
            }
        }
    '''
    TEST_UPDATE_USER_ARTICLE = '''
        mutation UpdateUserArticle( $pk: ID!, $title: String!, $content: String! ){
            updateUserArticle( pk: $pk, title: $title, content: $content ){
                state
            }
        } 
    '''
    TEST_QUERY_USER_ARTICLE = '''
        query GetUserArticle( $pk: ID ){
            userArticle( pk: $pk ){
                title
                content
                author{
                    username
                }
            }
        }
    '''
    TEST_CREATE_HOME_ARTICLE = '''
        mutation CreateHomeArticle( $title: String! , $preview: String! ,$content: String! ){
            createHomeArticle( title: $title, preview: $preview, content: $content ){
                slug
            }
        }
    '''
    TEST_UPDATE_HOME_ARTICLE = '''
        mutation UpdateHomeArticle( $slug: String!, $title: String!, $content: String!, $preview: String!, $disable: Boolean!){
            updateHomeArticle( slug: $slug, title: $title, content: $content, preview: $preview, disable: $disable ){
                slug
            }
        } 
    '''
    TEST_QUERY_HOME_ARTICLE = '''
        query GetHomeArticle( $slug: ID ){
            homeArticle( slug: $slug ){
                title
                content
                preview
                author{
                    username
                }
            }
        }
    '''
    TEST_UPDATE_ARTICLE_RECORD = '''
        mutation updateArticleRecord($pk: ID!){
            updateArticleRecord( pk : $pk ){
                state
            }
        }
    '''
    TEST_QUERY_ARTICLE_RECORD = '''
        query GetHomeArticleRecord( $slug: ID ){
            homeArticle( slug: $slug ){
                record {
                    count
                }
            }
        }
    '''

    def setUp(self):
        self.mock_usr = create_mock_user(self.TEST_MOCK_USERNAME, self.TEST_MOCK_PASSWORD)

    def test_create_and_update_user_article(self):
        client = get_test_graphql_client()
        context = get_query_context()
        context.user = self.mock_usr
        response = client.execute(
            self.TEST_CREATE_USER_ARTICLE,
            variables={
                'title': 'Previous',
                'content': ''
            },
            context_value=context,
        )
        article = get_object_or_None(UserArticle, title='Previous')
        assert article and article.pk == int(response.get('data').get('createUserArticle').get('pk'))
        response = client.execute(
            self.TEST_QUERY_USER_ARTICLE,
            variables={
                'pk': article.pk,
            },
            context_value=context
        )
        assert response.get('data').get('userArticle') == {
            'title': 'Previous',
            'content': '',
            'author': {
                'username': self.TEST_MOCK_USERNAME
            }
        }
        response = client.execute(
            self.TEST_UPDATE_USER_ARTICLE,
            variables={
                'pk': article.pk,
                'title': self.TEST_ARTICLE_TITLE,
                'content': self.TEST_ARTICLE_CONTENT
            },
            context_value=context
        )
        assert response.get('data').get('updateUserArticle').get('state') is True
        response = client.execute(
            self.TEST_QUERY_USER_ARTICLE,
            variables={
                'pk': article.pk,
            },
            context_value=context
        )
        assert response.get('data').get('userArticle') == {
            'title': self.TEST_ARTICLE_TITLE,
            'content': self.TEST_ARTICLE_CONTENT,
            'author': {
                'username': self.TEST_MOCK_USERNAME
            }
        }

    def test_create_and_update_home_article(self):
        client = get_test_graphql_client()
        context = get_query_context()
        context.user = self.mock_usr
        perm = Permission.objects.get(content_type=ContentType.objects.get_for_model(HomeArticle),
                                      codename="add_homearticle")
        self.mock_usr.user_permissions.add(perm)
        perm = Permission.objects.get(content_type=ContentType.objects.get_for_model(HomeArticle),
                                      codename="change_homearticle")
        self.mock_usr.user_permissions.add(perm)
        self.mock_usr.save()
        client.execute(
            self.TEST_CREATE_HOME_ARTICLE,
            variables={
                'title': 'Previous',
                'content': '',
                'preview': ''
            },
            context_value=context,
        )
        article = get_object_or_None(HomeArticle, title='Previous')
        assert article
        response = client.execute(
            self.TEST_QUERY_HOME_ARTICLE,
            variables={
                'slug': article.slug,
            },
            context_value=context
        )
        assert response.get('data').get('homeArticle') == {
            'title': 'Previous',
            'content': '',
            'preview': '',
            'author': {
                'username': self.TEST_MOCK_USERNAME
            }
        }
        response = client.execute(
            self.TEST_UPDATE_HOME_ARTICLE,
            variables={
                'slug': article.slug,
                'title': self.TEST_ARTICLE_TITLE,
                'content': self.TEST_ARTICLE_CONTENT,
                'preview': self.TEST_ARTICLE_PREVIEW,
                'disable': False,
            },
            context_value=context
        )
        # After updated, refresh the slug
        article = get_object_or_None(HomeArticle, pk=article.pk)
        response = client.execute(
            self.TEST_QUERY_HOME_ARTICLE,
            variables={
                'slug': article.slug
            },
            context_value=context
        )
        assert response.get('data').get('homeArticle') == {
            'title': self.TEST_ARTICLE_TITLE,
            'content': self.TEST_ARTICLE_CONTENT,
            'preview': self.TEST_ARTICLE_PREVIEW,
            'author': {
                'username': self.TEST_MOCK_USERNAME
            }
        }

    def test_update_article_record(self):
        client = get_test_graphql_client()
        context = get_query_context()
        context.user = self.mock_usr
        perm = Permission.objects.get(content_type=ContentType.objects.get_for_model(HomeArticle),
                                      codename="add_homearticle")
        self.mock_usr.user_permissions.add(perm)
        self.mock_usr.save()
        response = client.execute(
            self.TEST_CREATE_HOME_ARTICLE,
            variables={
                'title': self.TEST_ARTICLE_TITLE,
                'content': self.TEST_ARTICLE_CONTENT,
                'preview': self.TEST_ARTICLE_PREVIEW
            },
            context_value=context,
        )
        article = HomeArticle.objects.get(slug=response.get('data').get('createHomeArticle').get('slug'))
        response = client.execute(
            self.TEST_UPDATE_ARTICLE_RECORD,
            variables={
                'pk': article.pk
            }
        )
        assert response.get('data').get('updateArticleRecord').get('state') is True
        response = client.execute(
            self.TEST_QUERY_ARTICLE_RECORD,
            variables={
                'slug': article.slug
            }
        )
        assert response.get('data').get('homeArticle').get('record').get('count') == 1


class ArticleCommentTest(TestCase):
    TEST_MOCK_USERNAME = "TESTING-USERNAME"
    TEST_MOCK_PASSWORD = "TESTING-PASSWORD"
    TEST_CONTENT = 'This is reply comment test template'
    TEST_CREATE_USER_ARTICLE = '''
        mutation CreateUserArticle( $title: String! , $content: String! ){
            createUserArticle( title: $title, content: $content ){
                pk
            }
        }
    '''
    TEST_CREATE_ARTICLE_COMMENT = '''
        mutation CreateArticleComment( $pk: ID!, $content: String!, $reply: ID ){
            createArticleComment(pk: $pk, content: $content, reply: $reply){
                pk
            }
        }
    '''
    TEST_UPDATE_ARTICLE_COMMENT = '''
        mutation UpdateBaseReply( $pk: ID!, $content: String! ){
            updateBaseReply(pk: $pk, content: $content){
                state
            }
        }
    '''

    def setUp(self):
        self.mock_usr = create_mock_user(self.TEST_MOCK_USERNAME, self.TEST_MOCK_PASSWORD)

    def create_test_article(self):
        client = get_test_graphql_client()
        context = get_query_context()
        context.user = self.mock_usr
        res = client.execute(
            self.TEST_CREATE_USER_ARTICLE,
            variables={
                'title': 'TestTitle',
                'content': 'TestContent',
            },
            context_value=context
        )
        return UserArticle.objects.get(pk=res.get('data').get('createUserArticle').get('pk'))

    def test_create_and_update_article_comment(self):
        client = get_test_graphql_client()
        context = get_query_context()
        context.user = self.mock_usr
        article = self.create_test_article()
        response = client.execute(
            self.TEST_CREATE_ARTICLE_COMMENT,
            variables={
                'pk': article.pk,
                'content': 'TestContent'
            },
            context_value=context
        )
        pk = response.get('data').get('createArticleComment').get('pk')
        assert pk is not None
        response = client.execute(
            self.TEST_UPDATE_ARTICLE_COMMENT,
            variables={
                'pk': pk,
                'content': 'TestContent2'
            },
            context_value=context
        )
        assert response.get('data').get('updateBaseReply').get('state') is True
        assert ArticleComment.objects.get(pk=pk).content == 'TestContent2'

    def test_create_comment_with_reply(self):
        client = get_test_graphql_client()
        context = get_query_context()
        context.user = self.mock_usr
        article = self.create_test_article()
        response = client.execute(
            self.TEST_CREATE_ARTICLE_COMMENT,
            variables={
                'pk': article.pk,
                'content': 'Parent'
            },
            context_value=context
        )
        parent = response.get('data').get('createArticleComment').get('pk')
        assert parent is not None
        response = client.execute(
            self.TEST_CREATE_ARTICLE_COMMENT,
            variables={
                'pk': article.pk,
                'content': 'Child',
                'reply': parent
            },
            context_value=context
        )
        child = response.get('data').get('createArticleComment').get('pk')
        assert child is not None
        assert ArticleComment.objects.get(pk=child).reply.pk == int(parent)
