# Microsoft Graph API Email Setup Guide

This guide will help you set up Microsoft Graph API to send emails from your Azure tenant organization, replacing the SMTP functionality that your organization has restricted.

## Prerequisites

- Admin access to Azure Portal
- An Azure tenant with email accounts
- Permission to register applications in Azure AD

## Step-by-Step Setup

### 1. Register an Application in Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Fill in the details:
   - **Name**: `Daisy Valuation Email Service` (or any descriptive name)
   - **Supported account types**: `Accounts in this organizational directory only`
   - **Redirect URI**: Leave blank for this application type
5. Click **Register**

### 2. Configure API Permissions

1. In your registered app, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Application permissions** (not Delegated)
5. Search for and select **Mail.Send**
6. Click **Add permissions**
7. **IMPORTANT**: Click **Grant admin consent for [Your Organization]**
   - This requires Azure AD admin privileges
   - The permission status should show "✓ Granted for [Your Organization]"

### 3. Create a Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description: `Daisy Email Service Secret`
4. Set expiration (recommend 24 months)
5. Click **Add**
6. **IMMEDIATELY COPY** the secret value - you won't be able to see it again!

### 4. Gather Required Information

You'll need these values for your environment variables:

- **Tenant ID**: Found in **Overview** > **Directory (tenant) ID**
- **Client ID**: Found in **Overview** > **Application (client) ID**
- **Client Secret**: The value you copied in step 3
- **Sender Email**: The email address that will send emails (must be in your Azure tenant)

### 5. Set Environment Variables

Create a `.env` file in your project root or set these environment variables:

```bash
TENANT_ID=your-tenant-id-here
CLIENT_ID=your-client-id-here
CLIENT_SECRET=your-client-secret-here
SENDER_EMAIL=your-sender-email@yourdomain.com
BCC_EMAILS=admin@yourdomain.com,backup@yourdomain.com
```

**Note**: `BCC_EMAILS` is optional. If you want to receive copies of all valuation reports, add one or more comma-separated email addresses.

**Security Note**: Never commit the `.env` file to version control!

### 6. Verify Sender Email

The sender email address must:

- Be a valid email in your Azure tenant
- Have a mailbox (not just an alias)
- Be accessible by the service (some organizations restrict service account access)

### 7. Configure BCC Recipients (Optional)

You can automatically send copies of all valuation reports to additional email addresses:

1. **Single BCC Email**:

   ```bash
   BCC_EMAILS=admin@yourdomain.com
   ```

2. **Multiple BCC Emails** (comma-separated):

   ```bash
   BCC_EMAILS=admin@yourdomain.com,manager@yourdomain.com,backup@yourdomain.com
   ```

3. **No BCC Emails** (leave blank or omit):
   ```bash
   # BCC_EMAILS=
   ```

**Important Notes**:

- All BCC email addresses must be valid
- Invalid email addresses will be automatically filtered out
- BCC recipients will receive the same PDF attachment as the primary recipient
- BCC recipients won't be visible to the primary recipient

## Testing the Setup

1. Install the new dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run your Streamlit application:

   ```bash
   streamlit run valuation_app.py
   ```

3. Test the email functionality by:
   - Filling out the valuation form
   - Clicking "Email me my valuation report"
   - Check for successful sending or error messages

## Troubleshooting

### Common Issues

1. **"Failed to acquire token"**

   - Verify Tenant ID and Client ID are correct
   - Ensure Client Secret hasn't expired
   - Check that the app registration exists

2. **"Insufficient privileges"**

   - Ensure Mail.Send permission is granted
   - Admin consent must be given for application permissions
   - Verify you're using Application permissions, not Delegated

3. **"User not found" or "Mailbox not found"**

   - Verify the sender email exists in your tenant
   - Ensure the email has an active mailbox
   - Check that the email address format is correct

4. **"Access denied"**
   - The sender email may not have permission to send emails
   - Some organizations have additional policies restricting service accounts

### Debug Tips

- Enable detailed error logging in the application
- Test with different sender email addresses in your tenant
- Verify permissions in Azure Portal match the requirements
- Check Azure AD audit logs for authentication attempts

## Security Best Practices

1. **Client Secret Management**:

   - Store secrets securely (Azure Key Vault recommended for production)
   - Rotate secrets regularly
   - Never expose secrets in code or logs

2. **Least Privilege**:

   - Only grant Mail.Send permission (don't add unnecessary permissions)
   - Use application permissions instead of delegated when possible

3. **Monitoring**:
   - Monitor application usage in Azure AD
   - Set up alerts for authentication failures
   - Regular audit of app permissions

## Production Deployment

For production environments:

1. Use Azure Key Vault for secret management
2. Implement proper logging and monitoring
3. Set up health checks for the email service
4. Consider implementing retry logic for transient failures
5. Set up alerts for email delivery failures

## Additional Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [Mail API Reference](https://docs.microsoft.com/en-us/graph/api/user-sendmail)
- [Azure App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
