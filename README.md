# StyleGAN2 training on Studio Ghibli video frames

This is *only the data processing part* for generating latent space walks through video frames.

First, selected images were scraped from the Studio Ghibli Japan website (`screen_scrape.ipynb`)

A [RunwayML](https://runwayml.com/) StyleGAN2 (NVIDIA) model is pre-trained on 70k+ illustrations from Wikipedia, then trained on selected Ghibli video frames.

![](http://dev.universalities.com/ghibli/selected_v_green.png)

Model workspaces allow user input navigation through latent space to ‘optimal’ images

![](http://dev.universalities.com/ghibli/img_selection_green.png)

Preprocessing allows selection of only certain video frames based on HSL values via K-means pixel clustering

![](http://dev.universalities.com/ghibli/hsl.png)
![](http://dev.universalities.com/ghibli/cool_frames.png)
![](http://dev.universalities.com/ghibli/warm_frames.png)

Workspace exploration allows evolutionary development of images; by selecting ‘preferred’ images, it is possible to navigate through latent space iteratively to optimize images

Images can then be downloaded via the model workspace

![](http://dev.universalities.com/ghibli/img_selection.png)

Latent walk videos are generated via GPU on RunwayML using linear interpolation between selected or random frames:

![](http://dev.universalities.com/ghibli/linear_interp_video.png)

[![Video on YouTube](http://dev.universalities.com/ghibli/video_thumb.png)](https://www.youtube.com/watch?v=N6O4oKaZiCE "Studio Ghibli Latent Walk")

### FAQ

#### How much does it cost?

Training image models on RunwayML is $0.005 per step, so $15 to train for 3k steps (took about 4 hours). Generating a latent walk video on GPU using linear interpolation is costs $0.05 per minute (running time), so for a 4-minute video it was about ~$8 and took about 2.5 hours. So, 6 hours and $23 total -- not cheap, but good for a first-time experimenter looking to use a no-code environment. If I make more in the future, I'll probably use TensorFlow to train the model from the NVIDIA StyleGAN2, and run on another cloud compute GPU system ([Google GPU prices](https://cloud.google.com/compute/gpus-pricing)). StyleGAN2 is open source, [here](https://github.com/NVlabs/stylegan2)
