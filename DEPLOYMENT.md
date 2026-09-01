# Deployment & GitHub App setup (quickstart)

1) Create a GitHub Organization (ResQconnect) and ensure you have admin rights.
2) Create a GitHub App under the organization:
   - Settings → Developer settings → GitHub Apps → New GitHub App
   - Name: ResQconnect Aegis Treasury
   - Webhook URL: https://<your-host>/webhook
   - Webhook secret: generate a strong secret and add to .env / GitHub Secrets
   - Permissions:
     - Marketplace (read-only)
     - Metadata (read-only)
   - Subscribe to events: marketplace_purchase, marketplace_change, marketplace_cancelled
   - Generate a private key and download it (store securely)

3) Add secrets to GitHub repository (Settings → Secrets & variables → Actions):
   - GITHUB_WEBHOOK_SECRET
   - GITHUB_APP_ID
   - GITHUB_PRIVATE_KEY (or path via deployment secret vault)
   - JWT_SIGNING_KEY

4) Local testing with ngrok:
   - ngrok http 8000
   - Set the ngrok URL as the webhook URL in your GitHub App (for testing)
   - Use `curl` to POST test payloads and verify signature handling

5) Trigger a manual provisioning flow by simulating a marketplace_purchase event. The webhook skeleton will log and return 200 OK.


