from ckan.logic import auth_allow_anonymous_access

@auth_allow_anonymous_access
def taxonomy_list(context=None, data_dict=None):
    """
    Does the user have permission to list the taxonomies available.
    This is always yes.
    """
    return {'success': True}


@auth_allow_anonymous_access
def taxonomy_show(context=None, data_dict=None):
    """
    Can the user view a specific taxonomy
    This is always yes.
    """
    return {'success': True}

@auth_allow_anonymous_access
def taxonomy_create(context=None, data_dict=None):
    """
    Can the user create a new taxonomy.  This is only available to
    system administrators.

    There is a shortcut where this will not be called for sysadmins
    """
    return {'success': False}

@auth_allow_anonymous_access
def taxonomy_update(context=None, data_dict=None):
    """
    Can the user update an existing taxonomy.  This is only available to
    system administrators.

    There is a shortcut where this will not be called for sysadmins
    """
    return {'success': False}

@auth_allow_anonymous_access
def taxonomy_delete(context=None, data_dict=None):
    """
    Can a user delete a taxonomy.  System administrators only.

    There is a shortcut where this will not be called for sysadmins
    """
    return {'success': False}

@auth_allow_anonymous_access
def taxonomy_term_list(context=None, data_dict=None):
    """
    Can a user list taxonomy terms.
    """
    return {'success': True}

@auth_allow_anonymous_access
def taxonomy_term_tree(context=None, data_dict=None):
    """
    Can a user retrieve the terms for a taxonomy as a tree.
    """
    return {'success': True}


@auth_allow_anonymous_access
def taxonomy_term_show(context=None, data_dict=None):
    """
    Can a user view a taxonomy term (and the items using it)
    """
    return {'success': True}

@auth_allow_anonymous_access
def taxonomy_term_create(context=None, data_dict=None):
    """
    Can a user create a new taxonomy term.  Currently only system
    administrators

    There is a shortcut where this will not be called for sysadmins
    """
    return {'success': False}

@auth_allow_anonymous_access
def taxonomy_term_update(context=None, data_dict=None):
    """
    Can a user update an existing term.  Only system administrators

    There is a shortcut where this will not be called for sysadmins
    """
    return {'success': False}

@auth_allow_anonymous_access
def taxonomy_term_delete(context=None, data_dict=None):
    """
    Can a user delete a taxonomy term. System administrators only

    There is a shortcut where this will not be called for sysadmins
    """
    return {'success': False}

