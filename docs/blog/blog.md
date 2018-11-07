# Blog: Visual Search for Stolen Artworks

**TOM DOYLE**

## Blog One : The Idea

In this blog I hope to explore how my idea has come into fruition and where it stems from. The project is to be able to identify if an image is visually similar enough to be called the same image. This would use several image vision algorithms and would ideally be automatic. But what do I mean by automatic? I mean that you should be able to check one image against a database of hundreds or thousands. Ideally you could have regular checks run weekly or monthly to find a stolen images. 

There is also the question of where does the database come from. This is also a problem. I hope to implement a rudimentary web crawler to collect metadata about the images and where it has seen the image. By pre computing the information on the way into the database I hope this will speed up the final solution. In response to the question "Are you going to download every image on the internet?" No, I am not. Ideally you would start with the most popular sites and work down to the less popular ones. This is because the more people that see the stolen image, to more revenue the original owner stands to lose out on.

It is an idea that I have been curious about for quite a while and would love to see a solution to. I know a lot of photographers would also be interested in finding a solution to this problem as it stops many great photographers sharing their most prised images online. It also hurts online sales when you can see an image of the image before you buy the image. It leads to photographers putting heavy watermarks on their images and going through great lengths to stop them being used elsewhere. 

Other solutions out there may include reverse image search, such as Google's solution. I have researched these implementations and they seem to have more emphasis on semantic matching, meaning if you searched for an image of an orange cat in a tree it would be less concerned with that cat in that tree but more so any orange cat in any tree. The context matters but the specific subject can change. This is not what I want to implement. I was to compare the visual similarity of these images and be able to say with a percentage of confidence that the first image is the exact same image. 

You could just say why can't you take the hash of both of the images? But this is not ideal because even if one pixel of the image is changed the hashes won't match. This means the stolen images could elude the system if a watermark was added, the hue was changed or even if it was cropped the smallest amount. There is also another solution were you can match several histograms based on RGB values, textures and vectors. This solution can deal with small amounts of cropping but a watermark of hue will fool the solution into being a different image. 

In the next blog I will go into a proposed immature solution, and one that I will attempt to deploy. 


## My Second Blog Entry

This week, I learned how to include
[images](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#images)
in my blog.

![cat](https://gitlab.computing.dcu.ie/sblott/2018-ca400-XXXX/raw/master/docs/blog/images/cat.jpg)

Here are the instructions:

- Add the image to your repo (probably using the `images` sub-directory here).
  The cat example above is in `./images/cat.jpg`.

- Commit that and push it to your repo.

- On Gitlab, navigate to your new image and click *Raw*.  You get the raw URL of your image.  Copy that URL.

- Add your image to this document using the following format:

    <pre>![alternative text](URL)</pre>

See the example [here](https://gitlab.computing.dcu.ie/sblott/2018-ca400-XXXX/raw/master/docs/blog/blog.md).

You can also mention other users (like me: @sblott).

## Including Code

Raw text:
```
Mary had a little lamb,
it's fleece was white as snow.
```

Syntax highlighting is also possible; for example...

Python:
```python
i = 0
while i < len(s):
   # So something.
   i = i + 1
```

Java:
```java
for (i=0; i<s.length(); i+=1) {
   // Do something.
}
```

Coffeescript:
```coffeescript
i = 0
while i < s.length
   # So something.
   i = i + 1
```

## Instructions

Once you've understood this sample, replace it with your own blog.
