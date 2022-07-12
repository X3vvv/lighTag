# lighTag
lighTag UWB project

# Development

## [:art:](https://gist.github.com/rxaviers/7360908) UI
Using kivy library.

## [:page_with_curl:](https://gist.github.com/rxaviers/7360908) TODO
- [x] :bangbang: add floor layer number onto screen
- [ ] :bangbang: change base function into target area function, used to detect whether label has entered the area (use area color + voice to indicate whether has entered or not)
- [ ] :exclamation: imporove math function speed
- [ ] :exclamation: draw base position according to the beckend.py file's settings
- [ ] :exclamation: canvas range represent + x-y revert
- [X] :exclamation: red dot -> larger
- [ ] old dot fade out
- [ ] (optional) increase refresh rate
- [ ] (optional) add background (change along with floor level)
- [ ] ~~(abandoned) scale change according to base coords~~

## [:lollipop:](https://gist.github.com/rxaviers/7360908) General Steps
1. label gets distance data to each base
2. label transmits distance data to python program via wifi
3. python program to estimate label coordinates from distance information
4. python program draws the motion path of the coordinates
5. python program packaged to Android phone
