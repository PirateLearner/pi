from dash.base import BaseDashboardLayout, BaseDashboardPlaceholder
from dash.base import layout_registry


class ExampleMainPlaceholder(BaseDashboardPlaceholder):
    uid = 'main' # Unique ID of the placeholder.
    cols = 6 # Number of columns in the placeholder.
    rows = 5 # Number of rows in the placeholder.
    cell_width = 150 # Width of a single cell in the placeholder.
    cell_height = 110 # Height of a single cell in the placeholder.
    
class ExampleShortcutsPlaceholder(BaseDashboardPlaceholder):
    uid = 'shortcuts' # UID of the placeholder.
    cols = 1 # Number of columns in the placeholder.
    rows = 10 # Number of rows in the placeholder.
    cell_width = 60 # Width of a single cell in the placeholder.
    cell_height = 55 # Height of a single cell in the placeholder.
    
class ExampleLayout(BaseDashboardLayout):
    uid = 'example' # Layout UID.
    name = 'Example' # Layout name.

    # View template. Master template used in view mode.
    view_template_name = 'example/view_layout.html'

    # Edit template. Master template used in edit mode.
    edit_template_name = 'example/edit_layout.html'

    # All placeholders listed. Note, that placeholders are rendered in the
    # order specified here.
    placeholders = [ExampleMainPlaceholder, ExampleShortcutsPlaceholder]

    # Cell units used in the entire layout. Allowed values are: 'px', 'pt',
    # 'em' or '%'. In the ``ExampleMainPlaceholder`` cell_width is set to 150.
    #  It means that in this particular case its' actual width would be `150px`.
    cell_units = 'px'

    # Layout specific CSS.
    media_css = ('css/dash_layout_example.css',)

    # Layout specific JS.
    media_js = ('js/dash_layout_example.js',)

# Registering the layout.
layout_registry.register(ExampleLayout)