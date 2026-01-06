# Hockey Face Swap 🏒

An AI-powered web app that swaps hockey players' faces onto new team jerseys using InsightFace technology.

## Features

- Upload two images: player headshot and jersey template
- AI automatically detects and swaps faces
- Download the result instantly
- Clean, professional web interface
- Works with TIF, JPG, PNG files

## How to Deploy on Railway

### Step 1: Push to GitHub

1. Create a new repository on GitHub (don't initialize with README)
2. In your terminal, navigate to this project folder
3. Run these commands:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your hockey-face-swap repository
5. Railway will automatically detect it's a Python app
6. Click "Deploy"

### Step 3: Wait for Deployment

- First deployment takes 5-10 minutes (downloading AI models)
- Railway will provide you with a URL like `https://your-app.railway.app`
- Click the URL to access your app!

## Local Development (Optional)

To run locally:

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## How It Works

1. **Upload Player Headshot**: The face you want to use
2. **Upload Jersey Template**: Any photo of someone wearing the target team's jersey
3. **Click Swap**: AI detects faces and swaps them intelligently
4. **Download**: Get your result!

## Technical Details

- **Backend**: Flask (Python web framework)
- **Face Detection**: InsightFace Buffalo_L model
- **Face Swapping**: INSwapper 128 ONNX model
- **Image Processing**: OpenCV
- **Hosting**: Railway

## Tips for Best Results

- Use high-quality, well-lit headshots
- Make sure faces are clearly visible in both images
- Front-facing photos work better than side angles
- Similar lighting conditions between images produce better results

## Troubleshooting

**"No face detected" error:**
- Make sure the face is clearly visible and not obscured
- Try a different photo with better lighting
- Ensure the image isn't too small or low quality

**Slow processing:**
- First request after deployment is slower (model loading)
- Subsequent requests are faster
- Processing typically takes 10-30 seconds

**Deployment issues:**
- Railway free tier has some limitations
- Check Railway logs for specific error messages
- Models download on first deployment (takes time)

## Credits

Built with:
- [InsightFace](https://github.com/deepinsight/insightface) for face analysis
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [OpenCV](https://opencv.org/) for image processing

## License

MIT License - feel free to use and modify!
