from os import name
import sqlite3
import random
from rich import box
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.traceback import install
from collections import Counter
def main():
    install()
    def delete_menu_name(remove_name):
        conn = sqlite3.connect('FoodMenu.db')
        c = conn.cursor()
        c.execute("DELETE from food_all where menu_name=?", (remove_name,))
        c.execute("DELETE from spicy where menu_name=?", (remove_name,))
        c.execute("DELETE from japanese where menu_name=?", (remove_name,))
        c.execute("DELETE from chinese where menu_name=?", (remove_name,))
        c.execute("DELETE from soup where menu_name=?", (remove_name,))
        c.execute("DELETE from favorite where menu_name=?", (remove_name,))
        c.execute("DELETE from western where menu_name=?", (remove_name,))
        c.execute("DELETE from thai where menu_name=?", (remove_name,))
        c.execute("DELETE from dessert where menu_name=?", (remove_name,))
        conn.commit()
    console = Console()
    conn = sqlite3.connect('FoodMenu.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE if not exists dessert (
            menu_name text,
            menu_cal real
        )""")
    c.execute("""CREATE TABLE if not exists spicy (
            menu_name text,
            menu_cal real
        )""")
    c.execute("""CREATE TABLE if not exists thai (
            menu_name text,
            menu_cal real
        )""")
    c.execute("""CREATE TABLE if not exists chinese (
            menu_name text,
            menu_cal real
        )""")
    c.execute("""CREATE TABLE if not exists soup (
            menu_name text,
            menu_cal real
        )""")
    c.execute("""CREATE TABLE if not exists japanese (
            menu_name text,
            menu_cal real
        )""")
    c.execute("""CREATE TABLE if not exists western (
            menu_name text,
            menu_cal real
        )""")
    c.execute("""CREATE TABLE if not exists food_all (
            menu_name text,
            menu_cal real
        )""")
    c.execute("""CREATE TABLE if not exists favorite (
            menu_name text,
            menu_cal real
        )""")
    
    console = Console()
    conn = sqlite3.connect('FoodMenu.db')
    console.rule("[bold]GIN ARAI DEE")
    first_step = "default"
    table1= Table(title="Please Choose a Number", box = box.DOUBLE_EDGE)

    table1.add_column("Number", style="cyan")
    table1.add_column("Mode", style="green")

    table1.add_row("1", "Random")
    table1.add_row("2", "Add New Menu")
    table1.add_row("3", "Remove Menu")
    table1.add_row("4", "Print Everything In The Menu")
    table1.add_row("9", "!!RESET EVERYTHING!!")
    console.print(table1)
    try:
        console.print(Panel.fit("[bold]PLEASE ENTER [bold cyan]NUMBER[/bold cyan][/bold]"))
        first_step = int(console.input("👉 "))
    except ValueError:
        pass

    table2= Table(style="#e8e231", box = box.DOUBLE_EDGE)

    table2.add_column("1. Thai", justify="center", style="#e8e231")
    table2.add_column("2. Japanese", justify="center", style="#e8e231")
    table2.add_column("3. Chinese", justify="center", style="#e8e231")
    table2.add_column("4. Soup", justify="center", style="#e8e231")
    table2.add_row("[bold]5. Western","[bold]6. Spicy", "[bold]7. Favorite", "[bold]8. Dessert")

    if first_step == 1: #random menu
        console = Console()
        conn = sqlite3.connect('FoodMenu.db')
        c = conn.cursor()
        console.rule("[bold]Random Menu")
        console.print(table2)
        final_pick = []
        console.print(Panel.fit("Please pick the catagory, you may enter more than 1. For example: [yellow]spicy thai soup[/yellow] or [yellow]6 1 4 [/yellow][cyan](press Enter to skip)[/cyan]"))
        wanted_cat = input("👉 ").split(" ")
        console.print(Panel.fit("Please enter calory limit [cyan](press Enter to skip)[/cyan]"))
        calor_limit = input("👉 ")
        def send_to_final(items):
            if len(items) > 0:
                for i in items:
                    final_pick.append(i)
        if wanted_cat[0] == "":
            c.execute("SELECT * FROM food_all")
            send_to_final(c.fetchall())
        else:
            for j in range(len(wanted_cat)):
                if "spicy" == wanted_cat[j] or "6" == wanted_cat[j]:
                    c.execute("SELECT * FROM spicy")
                    send_to_final(c.fetchall())
                elif "dessert" == wanted_cat[j] or "8" == wanted_cat[j]:
                    c.execute("SELECT * FROM dessert")
                    send_to_final(c.fetchall())
                elif "thai" == wanted_cat[j] or "1" == wanted_cat[j]:
                    c.execute("SELECT * FROM thai")
                    send_to_final(c.fetchall())
                elif "chinese" == wanted_cat[j] or"3" == wanted_cat[j]:
                    c.execute("SELECT * FROM chinese")
                    send_to_final(c.fetchall())
                elif "soup" == wanted_cat[j] or "4" == wanted_cat[j]:
                    c.execute("SELECT * FROM soup")
                    send_to_final(c.fetchall())
                elif "favorite" == wanted_cat[j] or "7" == wanted_cat[j]:
                    c.execute("SELECT * FROM favorite")
                    send_to_final(c.fetchall())
                elif "western" == wanted_cat[j] or "5" == wanted_cat[j]:
                    c.execute("SELECT * FROM western")
                    send_to_final(c.fetchall())
                elif "japanese" == wanted_cat[j] or "2" == wanted_cat[j]:
                    c.execute("SELECT * FROM japanese")
                    send_to_final(c.fetchall())
                else:
                    console.print(Panel.fit("Sorry😓, I don't know a catagory name [yellow]"+ wanted_cat[j] + "[/yellow]", style="#d442f5")) 
        last_pick = dict(Counter(final_pick))
        out = []
        for k, v in last_pick.items():
            if v == len(wanted_cat):
                out.append(k)
        if len(out) == 0:
            console.print(Panel.fit("I can't find any menu that meet your request 🤔"))
        else:
            try:
                sort_cal = [i for i in out if i[1] <= int(calor_limit)]
                y = "default"
                try:
                    y = random.choice([e for e in sort_cal])
                except IndexError:
                    console.print(Panel.fit("Sorry😓, there is no Manu in this catagory that has calory less than [yellow]" + calor_limit + " [/yellow]kilocalorie 😭", style="#d442f5"))
                if y != "default":
                    console.print(Panel.fit("[green]How about [yellow]"+ y[0] +"[/yellow] 😋"+"\n"+"it will give you around [yellow]" +str(y[1])+ "[/yellow] kilocalorie[/green]", style="#e8e231", box = box.ROUNDED))
                    
            except ValueError:
                y = random.choice([e for e in out])
                console.print(Panel.fit("[green]How about [yellow]"+ y[0] +"[/yellow] 😋"+"\n"+"it will give you around [yellow]" +str(y[1])+ "[/yellow] kilocalorie[/green]", style="#e8e231", box = box.ROUNDED))
            conn.commit()
            conn.close()


    elif first_step == 2: #add menu
        console = Console()
        conn = sqlite3.connect('FoodMenu.db')
        c = conn.cursor()
        console.rule("[bold]Add New Menu")
        console.print(Panel.fit("[#f77f07]Enter your new menu here" + "\n" + "if the menu is already exist, all information of the old one will be replace" + "\n" + "👇👇👇[/#f77f07]", style="#f5d087"))
        new_menu_name = input().capitalize()
        console.print(table2)
        console.print(Panel.fit("[#f77f07]What catagoty is this?" + "\n" + "Btw, if you have more then 1 catagory, just leave a space between them 😉" + "\n" + "👇👇👇[/#f77f07]", style="#f5d087"))
        new_menu_cat =input().split(" ")
        console.print(Panel.fit("[#f77f07]Do you mind tell me the calory?" +"\n"+ "👇👇👇[/#f77f07]", style="#f5d087"))
        new_menu_cal = "default"
        while True:
            try:
                new_menu_cal = float(input())
                if new_menu_cal != "default":
                    break
            except ValueError:
                console.print(Panel.fit("[#f77f07]Can you give me in [yellow]NUMBER[/yellow] plzzz 😊[/#f77f07]", style="#f5d087"))
        delete_menu_name(new_menu_name)
        c.execute("INSERT INTO food_all VALUES (?, ?)", (new_menu_name, new_menu_cal))
        print(len(new_menu_cat))
        print(new_menu_cat)
        for i in range (len(new_menu_cat)):
            if new_menu_cat[i] == "spicy" or new_menu_cat[i] == "6":
                c.execute("INSERT INTO spicy VALUES (?, ?)", (new_menu_name, new_menu_cal))
            elif new_menu_cat[i] == "dessert" or new_menu_cat[i] == "8":
                c.execute("INSERT INTO dessert VALUES (?, ?)", (new_menu_name, new_menu_cal))
            elif new_menu_cat[i] == "thai" or new_menu_cat[i] == "1":
                c.execute("INSERT INTO thai VALUES (?, ?)", (new_menu_name, new_menu_cal))
            elif new_menu_cat[i] == "chinese" or new_menu_cat[i] == "3":
                c.execute("INSERT INTO chinese VALUES (?, ?)", (new_menu_name, new_menu_cal))
            elif new_menu_cat[i] == "soup" or new_menu_cat[i] == "4":
                c.execute("INSERT INTO soup VALUES (?, ?)", (new_menu_name, new_menu_cal))
            elif new_menu_cat[i] == "favorite" or new_menu_cat[i] == "7":
                c.execute("INSERT INTO favorite VALUES (?, ?)", (new_menu_name, new_menu_cal))
            elif new_menu_cat[i] == "western" or new_menu_cat[i] == "5":
                c.execute("INSERT INTO western VALUES (?, ?)", (new_menu_name, new_menu_cal))
            elif new_menu_cat[i] == "japanese" or new_menu_cat[i] == "2":
                c.execute("INSERT INTO japanese VALUES (?, ?)", (new_menu_name, new_menu_cal))
        console.print(Panel.fit("[#f77f07]✅ " + new_menu_name + "✅"+"\n"+ " has been added to "+ str(new_menu_cat) + "[#f77f07]", style="#f5d087"))
        conn.commit()
        conn.close()


    elif first_step == 3: #delete menu
        console = Console()
        conn = sqlite3.connect('FoodMenu.db')
        c = conn.cursor()
        console.rule("[bold]Delete Menu")
        console.print(Panel.fit("[white]Menu Name", style="#f06a5b"))
        print_del = input("👉 ").capitalize()
        delete_menu_name(print_del) 
        console.print(Panel.fit(print_del + "[white]" + " has been deleted", style="#f06a5b"))
        conn.commit()
        conn.close()
        
    elif first_step == 4:
        console = Console()
        conn = sqlite3.connect('FoodMenu.db')
        c = conn.cursor()
        console.rule("[bold]All Menu Available")
        def print_item(all_item, intro_message):
            var = dict(all_item)
            var2 = dict(sorted(var.items(), key=lambda x: x[1]))
            four_table = Table.grid(padding=1)
            four_table.add_column(style="green", justify="right")
            four_table.add_column(no_wrap=True)
            for i, j in var2.items():
                four_table.add_row(i ,str(j))
            console.print(Panel.fit(four_table, title="[b red]" + intro_message, border_style="bright_blue",))

            #var = dict(all_item)
            #var2 = dict(sorted(var.items(), key=lambda x: x[1]))
            #for i, j in var2.items():
            #    print(i, j)
            #print("")
        
        c.execute("SELECT * FROM food_all")
        all_item = c.fetchall()
        print_item(all_item, "All")

        c.execute("SELECT * FROM spicy")
        all_item = c.fetchall()
        print_item(all_item, "Spicy")

        c.execute("SELECT * FROM japanese")
        all_item = c.fetchall()
        print_item(all_item, "Japanese")

        c.execute("SELECT * FROM chinese")
        all_item = c.fetchall()
        print_item(all_item, "Chinese")

        c.execute("SELECT * FROM soup")
        all_item = c.fetchall()
        print_item(all_item, "Soup")

        c.execute("SELECT * FROM favorite")
        all_item = c.fetchall()
        print_item(all_item, "Favorite")

        c.execute("SELECT * FROM western")
        all_item = c.fetchall()
        print_item(all_item, "Western")

        c.execute("SELECT * FROM thai")
        all_item = c.fetchall()
        print_item(all_item, "Thai")

        c.execute("SELECT * FROM dessert")
        all_item = c.fetchall()
        print_item(all_item, "Dessert")
        conn.commit()
        conn.close()
        
    elif first_step == 9:
        console = Console()
        conn = sqlite3.connect('FoodMenu.db')
        c = conn.cursor()
        console.rule("[bold]RESET ALL")
        console.print(Panel(Align.center("[white]!!WARNING!!", style="white on red")))
        console.print(Panel.fit("⚠️  YOU ARE ABOUT TO RESET EVERYTHING, ALL DATA WILL BE DELETED ⚠️ " + "\n" + "[white]DO YOU WANT TO CONTINUE? (y/n/yes/no)[/white]", style="red"))
        confirmation = input("👉 ")
        if confirmation.upper() in ["YES", "Y", "NO", "N"]:
            if confirmation.upper() == "YES" or "Y":
                c.execute("DELETE FROM food_all")
                c.execute("DELETE FROM dessert")
                c.execute("DELETE FROM spicy")
                c.execute("DELETE FROM japanese")
                c.execute("DELETE FROM chinese")
                c.execute("DELETE FROM soup")
                c.execute("DELETE FROM favorite")
                c.execute("DELETE FROM thai")
                c.execute("DELETE FROM western")
            elif confirmation.upper() == "NO" or "N":
                print("RESET HAS BEEN CANCELED ")
        conn.commit()
        conn.close()
        

    elif first_step != 1 or 2 or 3 or 4 or 9:
        console.print(Panel.fit("ERROR: PLEASE ENTER ONLY 1,2,3,4 OR 9"), style="red")
    print(' ')
console = Console()
main()
while True:
    retern = console.input(Panel.fit("[bold]Press Enter[/bold] [white]to retern to first page[/white]", style="cyan"))
    if retern == '':
        main()