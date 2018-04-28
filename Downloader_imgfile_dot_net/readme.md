## How to use?

Well this is a particularly designed tool for downloading images from posts at i****-he****.nl(if you know it, you'll see it! ;-)

For those images uploaded to imgfile.net(a.k.a. PixSense, chaosimg, vestimage, etc.), you could batch download the pictures in a single post.

## Steps

1. first, right-click on the post to F12 to find the corresponding blockquote block;
2. second, copy element or ctrl-c to strip down the block of html code and paste it in a txt file;
3. run the scipt with Python3, key in the previous txt file name and the foldername which you want to save the images to under current directory;
4. [important & vulnerable] key in the initial letter of the model's name. e.g. PashaT -> p(non-case-sensitive)
5. images will therefore start to be downloaded. errors and faults will be yielded if necessary.

### step 4 above

This part is not fully tested, as I only downloaded 2 kinds of posts. Most of the files have a naming pattern like 'Name-Set-001.jpg', which works with my code. For those irregular filenames, I used a ordinal naming pattern '001.jpg'.

This part could cause trouble for other cases. Please alter as your will.
