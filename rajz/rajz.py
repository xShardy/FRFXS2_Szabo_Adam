import turtle

def pentagram(oldal=200):
    turtle.penup()
    turtle.goto(-oldal/2, -oldal/3)
    turtle.pendown()
    turtle.pencolor("black")
    turtle.pensize(3)

    for _ in range(5):
        turtle.forward(oldal)
        turtle.right(144)

def rajz():
    turtle.hideturtle()
    turtle.clear()
    pentagram(200)

# app
ablak = turtle.Screen()
ablak.title("Pentagram - 'd' rajzol, Esc kilép")


turtle.listen()
turtle.onkey(rajz, "d")
turtle.onkey(turtle.bye, "Escape")
turtle.mainloop()
