from odoo import api, SUPERUSER_ID

def set_default_multi_signature(env):
    """
    This function runs automatically after module installation or update.
    It sets multi_signature_1 as the default multi-signature.
    """
    try:
        # Get the multi-signature record using the XML reference
        multi_signature = env.ref('dept_wk.multi_signature_1', raise_if_not_found=False)

        if multi_signature:
            env['ir.config_parameter'].sudo().set_param('wk.default_signature', multi_signature.id)
            print(f"✅ Multi-signature {multi_signature.id} set as default")
        else:
            print("⚠️ Multi-signature XML reference not found.")
    except Exception as e:
        print(f"❌ Error setting default multi-signature: {e}")
