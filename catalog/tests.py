import unittest
import mock
from catalog.models import Category


class CategoryViewTest(unittest.TestCase):
    def test_category_view(self):
        mock_render_to_response = mock.Mock()
        mock_get_object_or_404 = mock.Mock()
        mock_category = mock.MagicMock()
        #category_name = "someCategoryName"
        #mock_category.name = category_name
        #mock_category.meta_keywords = "someMetaKeywords"
        #mock_category.meta_description = "someMetaKeywords"
        mock_get_object_or_404.return_value = mock_category

        with mock.patch.multiple('catalog.views',
                                 render_to_response=mock_render_to_response,
                                 get_object_or_404=mock_get_object_or_404,
                                 RequestContext=mock.Mock()):
            from catalog.views import show_category

            mock_request = mock.Mock()
            show_category(mock_request, category_slug="someCategorySlug")

            _, b, _ = mock_render_to_response.mock_calls[0]
            self.assertEqual(b[0], 'catalog/category.html')
            self.assertEqual(b[1]['meta_description'], mock_category.meta_description)
            self.assertEqual(b[1]['page_title'], mock_category.name)

