"""Utility methods for building patch
   operations. Each method returns an
   object for corresponding patch
   operation
"""

def patch_replace_op(field_path, value):
    """Build replace operation for patch
       request
    """
    replace_op = {'op': 'replace', 'path': field_path, 'value': value}
    return replace_op
