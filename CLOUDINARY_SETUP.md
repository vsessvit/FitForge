# Cloudinary Setup Guide for FitForge

## Quick Setup (5 minutes!)

Cloudinary is much easier than AWS S3 and perfect for this use case.

---

## Step 1: Create Cloudinary Account

1. Go to [cloudinary.com](https://cloudinary.com)
2. Click **Sign Up Free** (no credit card required!)
3. Complete registration
4. You'll be taken to your **Dashboard**

---

## Step 2: Get Your Cloudinary URL

On your Cloudinary Dashboard, you'll see:

```
API Environment variable
cloudinary://123456789012345:abcdefghijklmnopqrstuvwxyz-ABC@your-cloud-name
```

**Copy this entire URL** - this is all you need!

---

## Step 3: Configure Heroku

### Option A: Using Heroku CLI
```bash
heroku config:set CLOUDINARY_URL="cloudinary://123456789012345:abcdefghijklmnopqrstuvwxyz-ABC@your-cloud-name"
```

### Option B: Using Heroku Dashboard
1. Go to your Heroku app
2. Click **Settings** → **Config Vars** → **Reveal Config Vars**
3. Add:
   - **KEY**: `CLOUDINARY_URL`
   - **VALUE**: `cloudinary://123456789012345:abcdefghijklmnopqrstuvwxyz-ABC@your-cloud-name`
4. Click **Add**

---

## Step 4: Create Migration and Deploy

```bash
# Create migration for the model change
python manage.py makemigrations classes

# Commit all changes
git add .
git commit -m "Add Cloudinary for persistent media storage"

# Push to Heroku
git push heroku main
```

---

## Step 5: Re-upload Your Images

1. Go to your Heroku app admin: `https://your-app.herokuapp.com/admin/`
2. Navigate to **Classes** → **Fitness Classes**
3. Open each class
4. Upload the image in the **Image** field
5. Click **Save**

Images are now stored on Cloudinary and will **persist forever**! 🎉

---

##  Verify It's Working

1. After uploading, go to your Cloudinary dashboard
2. Click **Media Library** in the left menu
3. You should see a `classes/` folder with your images
4. Check your website - images should display correctly
5. Restart your Heroku dyno - images should still be there!

---

##  Free Tier Limits

Cloudinary Free Tier includes:
- ✅ **25 GB** Storage
- ✅ **25 GB** Monthly Bandwidth
- ✅ **25,000** Transformations/month
- ✅ **Automatic image optimization**
- ✅ **CDN delivery**
- ✅ **No credit card required**

This is more than enough for a fitness class website!

---

## 🔧 Local Development (Optional)

If you want to test Cloudinary locally:

1. Uncomment the Cloudinary line in your `env.py`:
```python
os.environ.setdefault('CLOUDINARY_URL', 'cloudinary://your-credentials')
```

2. Upload images through your local admin panel at `http://127.0.0.1:8000/admin/`

---

##  Troubleshooting

### Images still showing 404?
1. Check Heroku config: `heroku config` (should show CLOUDINARY_URL)
2. Check Heroku logs: `heroku logs --tail`
3. Make sure you **saved** after uploading images in admin
4. Try uploading one image and checking Cloudinary dashboard immediately

### Image URL looks weird?
- That's normal! Cloudinary URLs look like: `https://res.cloudinary.com/your-cloud/image/upload/v123456/classes/image.webp`
- They're served via CDN for fast loading worldwide

### Need to delete old images?
- Go to Cloudinary dashboard → Media Library
- Select images → Delete
- Or Django will replace them when you upload new ones with the same name

---

##  Done!

Your images are now:
- ✅ Stored permanently (not deleted on dyno restart)
- ✅ Optimized automatically
- ✅ Served via global CDN (fast loading)
- ✅ Free (within generous limits)
