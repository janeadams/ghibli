# StyleGAN2 training on Studio Ghibli video frames

![](http://dev.universalities.com/ghibli/ghibli_selected_interp_S.gif)

This is *only the data processing part* for generating latent space walks through video frames.

First, selected images were scraped from the Studio Ghibli Japan website (`screen_scrape.ipynb`)

![](http://dev.universalities.com/ghibli/files.png)

A [RunwayML](https://runwayml.com/) StyleGAN2 (NVIDIA) model is pre-trained on 70k+ illustrations from Wikipedia, then trained on selected Ghibli video frames.

![](http://dev.universalities.com/ghibli/ghibli_training.gif)

Model workspaces allow user input navigation through latent space to ‘optimal’ images

![](http://dev.universalities.com/ghibli/img_selection_green.png)

Preprocessing allows selection of only certain video frames based on HSL values via K-means pixel clustering
![](http://dev.universalities.com/ghibli/hsl.png)
![](http://dev.universalities.com/ghibli/cool_frames.png)
![](http://dev.universalities.com/ghibli/warm_frames.png)

Workspace exploration allows evolutionary development of images; by selecting ‘preferred’ images, it is possible to navigate through latent space iteratively to optimize images

Images can then be downloaded via the model workspace

![](http://dev.universalities.com/ghibli/img_selection.png)
