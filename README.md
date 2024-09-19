
# HPR (Human Personality Recognition)
## Important
 This code was written like 6 years ago, I was (15 y.o), this was a graduation project for one of my friends.
 all I am going to show here is my 6 y.o notes on how it works, and what struggles did I found along the way.
 don't expect me to understand the code, or even maintain it, its just there for anyone want to take a look at it.
## My notes
### the beginning
when i started at the project i had no idea what i was doing
because "opencv" was a new library (api) for me to learn
had it own cool functions that i got to mess around with
and even made my own!, ofc its not a 100% original function
idea but at least it made me write code that i can actually 
can read and understand for analysing errors and issues in general

### how the code work
its actually kinda simple to understand
first thing you need to input a dataset path
to the program that have to be sorted like this :-

dataset { -- input the path of this file
    class {
        photo.png
    }
}

after that the programing loop inside the classes folder
and get every single photo at a time, then we call an extraction function

### how extraction function work

#### main thread
we load the photo using cv2.imread(photo) to turn path into a np array that we can work with
after that we get every filter we need and make it inside class called "main"
after that we need to call a function inside the class called "start_process"
this function do all the work, first we start with calling cv2.findContours to get words
positions as a 2d array after that we call another class called "process" and what this class do 
is making this 2d array positions to rectangle, so i can make my life a bit easier
after that i am calling another class called "filter" and this is what everything actually 
starts what i do here is just things to remove any useless rectangle, to get better and 
accurate results, and how do i do that you ask ?, first thing we need to get rid of the 
threshold's filter generated dots + we need to get rid of any (. ,) to be identified as
a word or a letter, secound things we need to remove any rectangle that exist inside another
rectangle because if there is a bigger one at the same position why we keep the small one
too , right ?.
after that the "main thread" outputs our rectangle that been transformed from being 2d array 
to x and y + have been filtered for better results

#### (distances between words)=>(gets the output from main thread)
we simply make an empty array, and after that we loop inside the main thread's dilated_output
and we get one of the rectangle then we pass it inside another loop of the same 
main thread's output, and we get the lowest distance between the rectangle and another
and we add this to a the array we made and then we get the average of those distances

####  letter size
we're making an empty array, and after that we loop inside the main thread's treshold_output
and we get one of the rectangle then we get the rectangle area and we add it to the array
we made and then we calculate the average of those sizes

![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/letter_recognition.png?raw=true?raw=true "Title")

#### word size
we're making an empty array, and after that we loop inside the main thread's dilated_output
and we get one of the rectangle then we get the rectangle area and we add it to the array
we made and then we calculate the average of those sizes

#### word stroke
we're making an two empty array, and after that we loop inside the main thread's dilated_output (words)
then we loop inside it to the thread's threshold_output (letters) and we check if the 
small rectangle (the letter) is inside the big one (the word) then we add it to the first array
and after this we check if the len of the first array and after this we calculate distances between
the two nearest letters together and we loop that on all the letters we have on the first array
after this we add these distances on the secound array and then we repeat on all rectangles inside the 
main thread's dilated_output, and then we calculate the average of those distances

#### some outputs if you're interested
![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/output_example_1.png?raw=true "Title")
![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/output_example_2.png?raw=true "Title")
![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/output_example_3.png?raw=true "Title")
![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/output_example_4.png?raw=true "Title")

#### Strugles and changing plans while i was working on the project
i wanted to use the intersect method not only if there is rectangle inside another one
but also i wanted to be if the rectangle is toucing another rectangle then we merge these two
together but it had some big issues, first of all if what if i have three rectangles
but there is only two touching eachother but, if i merge them together the third one
gonna touch the rectangle that io just made, i had an easy sulotion for this 
code below (its not finished but i am going to say later why i didn't finish it):
```python
edit = False #this going to change to True if there is any intersect happend between two rectangles
recs = [] #this being the rectangle data the we get from findContours
while true: #making a loop until we remove any intersects
    Temp = [] #we need this to store our new rectangles on here first
    for x in recs:
        intersecting_rectangles = [] #to store the rectangles that intersect with the rectangle (x)
        intersecting_rectangles.append(x)
        for y in recs:
            if x != y: #to prevent checking itself
                if intersect(x, y):
                    edit = true
                    intersecting_rectangles.append(y)
        if len(intersecting_rectangles) > 1:
            Temp.append(make_new_rectangle(intersecting_rectangles))
        else:
            Temp.append(x)
    if not edit: break
    edit = False #reseting edit on the next loop
```
i didn't finish the code, because i found a problem with it, now if we're doing this loop
just to remove any intersect happening between words, then what if we have 2 words 
and every word have 3 rectangles but there is only two intersecting and the third one
going to intersect after we merge the other two together but if we merge it with the third one
its going to intersect with the other word, so we're basicly going to have a big rectangle
that contain two words together, and there is no way to prevent that, if you want to know 
more you can also check how i made a custom 2d array to rectangle function above, and you can 
also look at the photos for better demonstration

![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/my_problem.png?raw=true "Title")

#### Some equations you might be interested in
##### I have no idea what is that TBH but its looks like how i calculated distances between letters
![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/something_idk.png?raw=true "Title")
##### If rectangle is inside another
![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/is_inside_another.png?raw=true "Title")
##### If rectangle is intersecting with another
![alt text](https://github.com/DrunkTaric/hpr/blob/master/outputs/is_itersecting.png?raw=true "Title")
## Finally
If this was helpful to you in any way, drop a star :)
