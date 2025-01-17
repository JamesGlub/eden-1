# -*- coding: utf-8 -*-

"""
    Asset Management Functionality

    http://eden.sahanafoundation.org/wiki/BluePrint/Assets
"""

if not settings.has_module(c):
    raise HTTP(404, body="Module disabled: %s" % c)

# -----------------------------------------------------------------------------
def index():
    """ Module's Home Page """

    from s3db.cms import cms_index
    return cms_index(c, alt_function="index_alt")

# -----------------------------------------------------------------------------
def index_alt():
    """
        Module homepage for non-Admin users when no CMS content found
    """

    # Just redirect to the list of Assets
    s3_redirect_default(URL(f = "asset"))

# -----------------------------------------------------------------------------
def create():
    """ Redirect to asset/create """

    redirect(URL(f = "asset",
                 args = "create",
                 ))

# -----------------------------------------------------------------------------
def asset():
    """ RESTful CRUD controller """

    # Use the item() controller in this module to set options correctly
    s3db.asset_asset.item_id.comment = \
        S3PopupLink(f = "item",
                    label = T("Create Item"),
                    title = T("Item"),
                    tooltip = T("Type the name of an existing catalog item OR Click 'Create Item' to add an item which is not in the catalog."),
                    )

    # Defined in Model for use from Multiple Controllers for unified menus
    from s3db.asset import asset_controller
    return asset_controller()

# -----------------------------------------------------------------------------
def log():
    """
        RESTful CRUD controller for Asset Logs
        - just used for options.s3json lookups
    """

    s3.prep = lambda r: \
        r.representation == "s3json" and r.method == "options"

    return s3_rest_controller()

# -----------------------------------------------------------------------------
def brand():
    """ RESTful CRUD controller """

    return s3_rest_controller("supply", "brand")

# -----------------------------------------------------------------------------
def catalog():
    """ RESTful CRUD controller """

    from s3db.supply import supply_catalog_rheader
    return s3_rest_controller("supply", "catalog",
                              rheader = supply_catalog_rheader,
                              )

# -----------------------------------------------------------------------------
def item():
    """ RESTful CRUD controller """

    if "catalog_item" not in request.args:
        # Filter to just Assets
        table = s3db.supply_item
        ctable = s3db.supply_item_category
        s3.filter = (table.item_category_id == ctable.id) & \
                    (ctable.can_be_asset == True)

        # Limit the Categories to just those which can be Assets
        # - make category mandatory so that filter works
        field = s3db.supply_item.item_category_id
        field.requires = IS_ONE_OF(db, "supply_item_category.id",
                                   s3db.supply_item_category_represent,
                                   filterby = "can_be_asset",
                                   filter_opts = (True,),
                                   sort = True,
                                   )

        field.comment = S3PopupLink(f = "item_category",
                                    label = T("Create Item Category"),
                                    title = T("Item Category"),
                                    tooltip = T("Only Categories of type 'Asset' will be seen in the dropdown."),
                                    )

    # Defined in the Model for use from Multiple Controllers for unified menus
    from s3db.supply import supply_item_controller
    return supply_item_controller()

# -----------------------------------------------------------------------------
def catalog_item():
    """
        RESTful CRUD controller
        - used for Imports
    """

    return s3_rest_controller("supply", "catalog_item",
                              csv_template = ("supply", "catalog_item"),
                              csv_stylesheet = ("supply", "catalog_item.xsl"),
                              )

# -----------------------------------------------------------------------------
def item_category():
    """ RESTful CRUD controller """

    table = s3db.supply_item_category

    # Filter to just Assets
    s3.filter = (table.can_be_asset == True)

    # Default to Assets
    field = table.can_be_asset
    field.readable = field.writable = False
    field.default = True

    return s3_rest_controller("supply", "item_category")

# -----------------------------------------------------------------------------
def supplier():
    """ RESTful CRUD controller """

    get_vars["organisation_type.name"] = "Supplier"

    # Load model
    table = s3db.org_organisation

    # Modify CRUD Strings
    s3.crud_strings.org_organisation = Storage(
        label_create = T("Create Supplier"),
        title_display = T("Supplier Details"),
        title_list = T("Suppliers"),
        title_update = T("Edit Supplier"),
        title_upload = T("Import Suppliers"),
        label_list_button = T("List Suppliers"),
        label_delete_button = T("Delete Supplier"),
        msg_record_created = T("Supplier added"),
        msg_record_modified = T("Supplier updated"),
        msg_record_deleted = T("Supplier deleted"),
        msg_list_empty = T("No Suppliers currently registered"),
        )

    from s3db.org import org_organisation_controller
    return org_organisation_controller()

# -----------------------------------------------------------------------------
def telephone():
    """
        RESTful CRUD controller
        Filtered version of the asset_asset resource
    """

    tablename = "asset_asset"
    table = s3db[tablename]

    s3db.configure("asset_telephone",
                   deletable = False,
                   )

    # Type is Telephone
    from s3db.asset import asset_types
    TELEPHONE = asset_types["TELEPHONE"]
    field = table.type
    field.default = TELEPHONE
    field.readable = False
    field.writable = False

    # Only show telephones
    s3.filter = (field == TELEPHONE)

    # Remove type from list_fields
    list_fields = s3db.get_config("asset_asset", "list_fields")
    if "type" in list_fields:
        list_fields.remove("type")

    field = table.item_id
    field.label = T("Telephone Type")
    #field.widget = None # We want a simple dropdown, which is the default anyway
    field.comment = S3PopupLink(f = "item",
                                # Use this controller for options.json rather than looking for one called 'asset'
                                vars = {"parent": "telephone"},
                                label = T("Add Telephone Type"),
                                info = T("Add a new telephone type"),
                                title = T("Telephone Type"),
                                tooltip = T("Only Items whose Category are of type 'Telephone' will be seen in the dropdown."),
                                )

    # Only select from telephones
    ctable = s3db.supply_item_category
    telephone_categories = db(ctable.is_telephone == True).select(ctable.id)
    field.requires.set_filter(filterby = "item_category_id",
                              filter_opts = [row.id for row in telephone_categories],
                              )

    # CRUD strings
    s3.crud_strings[tablename] = Storage(
        label_create = T("Add Telephone"),
        title_display = T("Telephone Details"),
        title_list = T("Telephones"),
        title_update = T("Edit Telephone"),
        title_map = T("Map of Telephones"),
        label_list_button = T("List Telephones"),
        label_delete_button = T("Delete Telephone"),
        msg_record_created = T("Telephone added"),
        msg_record_modified = T("Telephone updated"),
        msg_record_deleted = T("Telephone deleted"),
        msg_list_empty = T("No Telephones currently registered"),
        )

    # @ToDo: Tweak the search comment

    # Defined in Model
    from s3db.asset import asset_controller
    return asset_controller()

# END =========================================================================
