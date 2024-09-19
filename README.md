
# HPR (Human Personality Recognition)
## Important
 This code was written like 5 years ago, this was a graduation project for one of my friends.
 all I am going to show here is my 5 y.o notes on how it works, and what struggles did I found along the way.
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

