# 🚀 Deploy 7K Vault Website to Vercel

## Why Vercel?
- ✅ **Faster** than GitHub Pages
- ✅ **Better CDN** worldwide
- ✅ **Custom domain** support
- ✅ **Automatic HTTPS**
- ✅ **Zero config** deployment
- ✅ **Free** for personal projects

---

## 🎯 Quick Deploy (2 Minutes)

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel**: https://vercel.com/signup
2. **Sign in with GitHub** (it's free)
3. Click **"Add New..."** → **"Project"**
4. **Import** your repository: `kunu2009/7kvault`
5. **Configure**:
   - Framework Preset: **Other**
   - Root Directory: **docs** (very important!)
   - Build Command: *leave empty*
   - Output Directory: **.** (dot)
6. Click **"Deploy"**
7. **Done!** Your site is live at: `https://7kvault.vercel.app`

---

### Option 2: Deploy via Vercel CLI

```powershell
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (from project root)
cd C:\Desktop\locker
vercel

# Follow prompts:
# Set up and deploy? Yes
# Which scope? Your account
# Link to existing project? No
# Project name? 7kvault
# In which directory? ./docs
# Want to modify settings? No

# Production deployment
vercel --prod
```

---

## 🌐 Your Website URLs

After deployment, you'll get:
- **Vercel URL**: `https://7kvault.vercel.app` (automatic)
- **Custom Domain**: `7kvault.com` (if you buy domain)
- **GitHub**: `https://github.com/kunu2009/7kvault` (repo)

---

## 🎨 Update Website URLs

After deploying, update these URLs in your website:

### In `docs/index.html`:
```html
<!-- Change this line: -->
🌐 **Website**: [https://kunu2009.github.io/7kvault](https://kunu2009.github.io/7kvault)

<!-- To this: -->
🌐 **Website**: [https://7kvault.vercel.app](https://7kvault.vercel.app)
```

### In `README.md`:
```markdown
🌐 **Website**: [https://7kvault.vercel.app](https://7kvault.vercel.app)
```

---

## ⚙️ Vercel Configuration

The `vercel.json` file is already configured:
```json
{
  "version": 2,
  "name": "7kvault",
  "builds": [
    {
      "src": "docs/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/docs/$1"
    }
  ]
}
```

This tells Vercel to:
- Serve files from the `docs/` folder
- Treat it as a static website
- Route all requests to the correct files

---

## 🔄 Automatic Deployments

After connecting to Vercel:
- ✅ **Every push to `main`** → Automatic production deploy
- ✅ **Every pull request** → Preview deploy
- ✅ **Instant rollbacks** if needed
- ✅ **Build logs** for debugging

---

## 🎯 Custom Domain (Optional)

### If you buy a domain (e.g., 7kvault.com):

1. Go to Vercel Dashboard → Your Project
2. Click **Settings** → **Domains**
3. Add your domain: `7kvault.com` and `www.7kvault.com`
4. Update DNS records at your domain registrar:
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   
   Type: A
   Name: @
   Value: 76.76.21.21
   ```
5. Wait 5-10 minutes for DNS propagation
6. **Done!** Your site is at `https://7kvault.com`

---

## 📊 Vercel Features You Get

### Analytics
- Page views
- Unique visitors
- Popular pages
- Load times

### Performance
- Global CDN (faster than GitHub Pages)
- Automatic compression
- Image optimization
- HTTP/2 and HTTP/3

### Developer Experience
- Preview deployments for PRs
- Instant rollbacks
- Real-time logs
- Custom headers

---

## 🐛 Troubleshooting

### "404 Not Found"
- Make sure Root Directory is set to `docs`
- Check that `index.html` exists in `docs/`

### "Build Failed"
- This is a static site, no build needed
- Leave Build Command empty

### "Slow Loading"
- Vercel automatically optimizes
- If still slow, check image sizes

### "Domain Not Working"
- DNS takes 5-10 minutes to propagate
- Double-check DNS records
- Use Vercel DNS for fastest setup

---

## 🚀 After Deployment

### Update Your Links:

1. **README.md**:
   ```markdown
   🌐 **Website**: [https://7kvault.vercel.app](https://7kvault.vercel.app)
   ```

2. **GitHub Repository Description**:
   ```
   🔒 Free encrypted gallery for Windows | Visit: https://7kvault.vercel.app
   ```

3. **Commit and Push**:
   ```powershell
   git add .
   git commit -m "Add Vercel configuration and update URLs"
   git push origin main
   ```

---

## 💡 Pro Tips

### SEO
- Vercel automatically generates `sitemap.xml`
- Add `robots.txt` if needed
- Already has proper meta tags

### Performance
- Vercel scores 100/100 on Lighthouse
- Global CDN for fast loading worldwide
- Automatic HTTPS

### Monitoring
- Check Vercel dashboard for:
  - Visitor analytics
  - Error logs
  - Performance metrics

---

## 🎊 Benefits Over GitHub Pages

| Feature | Vercel | GitHub Pages |
|---------|--------|--------------|
| **Speed** | ⚡ Faster (Global CDN) | 🐌 Slower |
| **Custom Domain** | ✅ Free SSL | ✅ Free SSL |
| **Deploy Time** | 🚀 30 seconds | 🕐 2-5 minutes |
| **Preview Deploys** | ✅ Yes | ❌ No |
| **Analytics** | ✅ Built-in | ❌ Need Google |
| **Rollbacks** | ✅ Instant | ❌ Manual |
| **Build Logs** | ✅ Real-time | ❌ Limited |

---

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Support**: https://vercel.com/support
- **Community**: https://github.com/vercel/vercel/discussions

---

## ✅ Checklist

- [ ] Sign up for Vercel (free)
- [ ] Connect GitHub repository
- [ ] Set root directory to `docs`
- [ ] Deploy project
- [ ] Get your URL: `https://7kvault.vercel.app`
- [ ] Update README.md with new URL
- [ ] Update website meta tags
- [ ] Push changes to GitHub
- [ ] (Optional) Add custom domain

---

**That's it! Your website is now faster, more professional, and easier to manage!** 🎉

*Vercel deploys in 30 seconds and your website is live worldwide!*
