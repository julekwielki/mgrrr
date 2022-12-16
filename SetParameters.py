from tkinter import *
from tkinter import messagebox


class SetParameters(object):

    def __init__(self, tab1, parametry, fun):
        self.parametry = parametry
        self.fun = fun

        # naturalna śmierć
        self.nat_death = LabelFrame(tab1, text="naturalna śmierć")  # ramka

        self.label_t = Label(self.nat_death, text='t')
        self.label_t.grid(row=0, column=1, padx=10, pady=2)

        self.t_n_d = Entry(self.nat_death)
        self.t_n_d.grid(row=0, column=2, padx=10, pady=2)
        self.t_n_d.config(width=10)
        self.t_n_d.insert(0, parametry[0])

        self.label_a = Label(self.nat_death, text='a')
        self.label_a.grid(row=1, column=1, padx=10, pady=2)

        self.a_n_d = Entry(self.nat_death)
        self.a_n_d.grid(row=1, column=2, padx=10, pady=2)
        self.a_n_d.config(width=10)
        self.a_n_d.insert(0, parametry[1])

        self.label_n = Label(self.nat_death, text='n')
        self.label_n.grid(row=2, column=1, padx=10, pady=2)

        self.n_n_d = Entry(self.nat_death)
        self.n_n_d.grid(row=2, column=2, padx=10, pady=2)
        self.n_n_d.config(width=10)
        self.n_n_d.insert(0, parametry[2])

        self.var_nat_death = IntVar()
        self.check_n_d = Checkbutton(self.nat_death, text="włączone", variable=self.var_nat_death, width=6,
                                     command=self.on_select)
        if self.fun[0] == 1:
            self.check_n_d.select()
        else:
            self.check_n_d.deselect()
        self.check_n_d.grid(row=0, column=3, padx=10, pady=10, rowspan=3)
        self.nat_death.grid(row=0, column=0, rowspan=3, columnspan=1, padx=10, pady=5)

        # rozmnazanie
        self.repr = LabelFrame(tab1, text="rozmnazanie")  # ramka

        self.label_c = Label(self.repr, text='c')
        self.label_c.grid(row=0, column=1, padx=10, pady=4)

        self.c_repr = Entry(self.repr)
        self.c_repr.grid(row=0, column=2, padx=10, pady=4)
        self.c_repr.config(width=10)
        self.c_repr.insert(0, parametry[3])

        self.var_repr = IntVar()  # wartość do checkbuttona
        self.check_repr = Checkbutton(self.repr, text="włączone", variable=self.var_repr, width=6,
                                      command=self.on_select)
        if self.fun[1] == 1:
            self.check_repr.select()
        else:
            self.check_repr.deselect()
        self.check_repr.grid(row=0, column=3, padx=10, pady=5)
        self.repr.grid(row=4, column=0, rowspan=1, columnspan=1, padx=10, pady=6)

        # pozostałe
        self.rest = LabelFrame(tab1, text="pozostałe efekty")  # ramka

        self.var_dam = IntVar()
        self.check_dam = Checkbutton(self.rest, text="uszkodzenie spontaniczne", variable=self.var_dam)
        if self.fun[2] == 1:
            self.check_dam.select()
        else:
            self.check_dam.deselect()
        self.check_dam.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.var_rad = IntVar()  # śmierć od radiacji
        self.check_rad = Checkbutton(self.rest, text="śmierć radiacyjna", variable=self.var_rad)
        if self.fun[3] == 1:
            self.check_rad.select()
        else:
            self.check_rad.deselect()
        self.check_rad.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.var_damr = IntVar()
        self.check_damr = Checkbutton(self.rest, text="uszkodzenie radiacyjne", variable=self.var_damr)
        if self.fun[4] == 1:
            self.check_damr.select()
        else:
            self.check_damr.deselect()
        self.check_damr.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        self.var_by = IntVar()
        self.check_by = Checkbutton(self.rest, text="efekt sąsiedztwa", variable=self.var_by)
        if self.fun[5] == 1:
            self.check_by.select()
        else:
            self.check_by.deselect()
        self.check_by.grid(row=3, column=0, padx=10, pady=5, rowspan=1, sticky='w')

        self.rest.grid(row=0, column=2, rowspan=5, padx=10, pady=5)

    def on_select(self):
        if self.var_nat_death.get():
            self.a_n_d.config(state='normal')
            self.n_n_d.config(state='normal')
            self.t_n_d.config(state='normal')
        else:
            self.a_n_d.config(state='disabled')
            self.n_n_d.config(state='disabled')
            self.t_n_d.config(state='disabled')

        if self.var_repr.get():
            self.c_repr.config(state='normal')
        else:
            self.c_repr.config(state='disabled')

    def reset(self, parametry):
        self.check_n_d.select()
        self.a_n_d.config(state='normal')
        self.n_n_d.config(state='normal')
        self.t_n_d.config(state='normal')
        self.check_repr.select()
        self.c_repr.config(state='normal')

        self.check_dam.select()
        self.check_rad.select()
        self.check_damr.select()
        self.check_by.select()

        self.t_n_d.delete(0, END)
        self.t_n_d.insert(0, parametry[0])
        self.a_n_d.delete(0, END)
        self.a_n_d.insert(0, parametry[1])
        self.n_n_d.delete(0, END)
        self.n_n_d.insert(0, parametry[2])
        self.c_repr.delete(0, END)
        self.c_repr.insert(0, parametry[3])

    def get_data(self):
        try:
            self.parametry[0] = float(self.t_n_d.get())
            self.parametry[1] = float(self.a_n_d.get())
            self.parametry[2] = float(self.n_n_d.get())
            self.parametry[3] = float(self.c_repr.get())
        except ValueError:
            messagebox.showinfo("uwaga", "Błędnie podany parametr - niepoprawny znak")

        a = [self.var_nat_death.get(), self.var_repr.get(), self.var_dam.get(), self.var_rad.get(),
             self.var_damr.get(), self.var_by.get()]
        return self.parametry, a


class SetParametersD(object):

    def __init__(self, tab1, parametry, fun):
        self.parametry = parametry
        self.fun = fun

        # naturalna śmierć
        self.nat_death = LabelFrame(tab1, text="naturalna śmierć")  # ramka

        self.label_t = Label(self.nat_death, text='t')
        self.label_t.grid(row=0, column=1, padx=10, pady=2)

        self.t_n_d = Entry(self.nat_death)
        self.t_n_d.grid(row=0, column=2, padx=10, pady=2)
        self.t_n_d.config(width=10)
        self.t_n_d.insert(0, parametry[0])

        self.label_a = Label(self.nat_death, text='a')
        self.label_a.grid(row=1, column=1, padx=10, pady=2)

        self.a_n_d = Entry(self.nat_death)
        self.a_n_d.grid(row=1, column=2, padx=10, pady=2)
        self.a_n_d.config(width=10)
        self.a_n_d.insert(0, parametry[1])

        self.label_n = Label(self.nat_death, text='n')
        self.label_n.grid(row=2, column=1, padx=10, pady=2)

        self.n_n_d = Entry(self.nat_death)
        self.n_n_d.grid(row=2, column=2, padx=10, pady=2)
        self.n_n_d.config(width=10)
        self.n_n_d.insert(0, parametry[2])

        self.var_nat_death = IntVar()
        self.check_n_d = Checkbutton(self.nat_death, text="włączone", variable=self.var_nat_death, width=6,
                                     command=self.on_select)
        if self.fun[0] == 1:
            self.check_n_d.select()
        else:
            self.check_n_d.deselect()
        self.check_n_d.grid(row=0, column=3, padx=10, pady=10, rowspan=3)
        self.nat_death.grid(row=0, column=0, rowspan=3, columnspan=1, padx=10, pady=5)

        # rozmnazanie
        self.repr = LabelFrame(tab1, text="rozmnazanie")  # ramka

        self.label_c = Label(self.repr, text='c')
        self.label_c.grid(row=0, column=1, padx=10, pady=2)

        self.c_repr = Entry(self.repr)
        self.c_repr.grid(row=0, column=2, padx=10, pady=2)
        self.c_repr.config(width=10)
        self.c_repr.insert(0, parametry[3])

        self.var_repr = IntVar()  # wartość do checkbuttona
        self.check_repr = Checkbutton(self.repr, text="włączone", variable=self.var_repr, width=6,
                                      command=self.on_select)
        if self.fun[1] == 1:
            self.check_repr.select()
        else:
            self.check_repr.deselect()
        self.check_repr.grid(row=0, column=3, padx=10, pady=2, rowspan=1)
        self.repr.grid(row=4, column=0, rowspan=1, columnspan=1, padx=10)

        # mutowanie
        self.mut = LabelFrame(tab1, text="mutowanie")  # ramka

        self.label_c = Label(self.mut, text='c')
        self.label_c.grid(row=0, column=1, padx=10, pady=2)

        self.c_mut = Entry(self.mut)
        self.c_mut.grid(row=0, column=2, padx=10, pady=2)
        self.c_mut.config(width=10)
        self.c_mut.insert(0, parametry[4])

        self.var_mut = IntVar()  # wartość do checkbuttona
        self.check_mut = Checkbutton(self.mut, text="włączone", variable=self.var_mut, width=6,
                                     command=self.on_select)
        if self.fun[2] == 1:
            self.check_mut.select()
        else:
            self.check_mut.deselect()
        self.check_mut.grid(row=0, column=3, padx=10, pady=2, rowspan=1)
        self.mut.grid(row=5, column=0, rowspan=1, columnspan=1, padx=10, pady=5)

        # pozostałe efekty
        self.rest = LabelFrame(tab1, text="pozostałe efekty")  # ramka

        self.var_dam = IntVar()
        self.check_dam = Checkbutton(self.rest, text="uszkodzenie spontaniczne", variable=self.var_dam)
        if self.fun[3] == 1:
            self.check_dam.select()
        else:
            self.check_dam.deselect()
        self.check_dam.grid(row=0, column=0, padx=10, pady=3, sticky='w')

        self.var_rep = IntVar()
        self.check_rep = Checkbutton(self.rest, text="naprawa", variable=self.var_rep)
        if self.fun[4] == 1:
            self.check_rep.select()
        else:
            self.check_rep.deselect()
        self.check_rep.grid(row=1, column=0, padx=10, pady=3, sticky='w')

        self.var_rad = IntVar()  # śmierć od radiacji
        self.check_rad = Checkbutton(self.rest, text="śmierć radiacyjna", variable=self.var_rad)
        if self.fun[5] == 1:
            self.check_rad.select()
        else:
            self.check_rad.deselect()
        self.check_rad.grid(row=2, column=0, padx=10, pady=3, sticky='w')

        self.var_damr = IntVar()
        self.check_damr = Checkbutton(self.rest, text="uszkodzenie radiacyjne", variable=self.var_damr)
        if self.fun[6] == 1:
            self.check_damr.select()
        else:
            self.check_damr.deselect()
        self.check_damr.grid(row=3, column=0, padx=10, pady=3, sticky='w')

        self.var_by = IntVar()
        self.check_by = Checkbutton(self.rest, text="efekt sąsiedztwa", variable=self.var_by)
        if self.fun[7] == 1:
            self.check_by.select()
        else:
            self.check_by.deselect()
        self.check_by.grid(row=4, column=0, padx=10, pady=3, rowspan=1, sticky='w')

        self.var_ad = IntVar()
        self.check_ad = Checkbutton(self.rest, text="odpowiedź adaptacyjna", variable=self.var_ad)
        if self.fun[8] == 1:
            self.check_ad.select()
        else:
            self.check_ad.deselect()
        self.check_ad.grid(row=5, column=0, padx=10, pady=3, rowspan=1, sticky='w')

        self.rest.grid(row=0, column=1, rowspan=6, padx=10, pady=5, sticky='n')

    def on_select(self):
        if self.var_nat_death.get():
            self.a_n_d.config(state='normal')
            self.n_n_d.config(state='normal')
            self.t_n_d.config(state='normal')
        else:
            self.a_n_d.config(state='disabled')
            self.n_n_d.config(state='disabled')
            self.t_n_d.config(state='disabled')

        if self.var_repr.get():
            self.c_repr.config(state='normal')
        else:
            self.c_repr.config(state='disabled')

        if self.var_mut.get():
            self.c_mut.config(state='normal')
        else:
            self.c_mut.config(state='disabled')

    def reset(self, parametry):
        self.check_n_d.select()
        self.a_n_d.config(state='normal')
        self.n_n_d.config(state='normal')
        self.t_n_d.config(state='normal')
        self.check_repr.select()
        self.c_repr.config(state='normal')
        self.check_mut.select()
        self.c_mut.config(state='normal')

        self.check_dam.select()
        self.check_rep.select()
        self.check_rad.select()
        self.check_damr.select()
        self.check_by.select()
        self.check_ad.select()

        self.t_n_d.delete(0, END)
        self.t_n_d.insert(0, parametry[0])
        self.a_n_d.delete(0, END)
        self.a_n_d.insert(0, parametry[1])
        self.n_n_d.delete(0, END)
        self.n_n_d.insert(0, parametry[2])
        self.c_repr.delete(0, END)
        self.c_repr.insert(0, parametry[3])
        self.c_mut.delete(0, END)
        self.c_mut.insert(0, parametry[4])

    def get_data(self):
        try:
            self.parametry[0] = float(self.t_n_d.get())
            self.parametry[1] = float(self.a_n_d.get())
            self.parametry[2] = float(self.n_n_d.get())
            self.parametry[3] = float(self.c_repr.get())
            self.parametry[4] = float(self.c_mut.get())
        except ValueError:
            messagebox.showinfo("uwaga", "Błędnie podany parametr - niepoprawny znak")

        a = [self.var_nat_death.get(), self.var_repr.get(), self.var_mut.get(), self.var_dam.get(),
             self.var_rep.get(), self.var_rad.get(), self.var_damr.get(), self.var_by.get(),
             self.var_ad.get()]
        return self.parametry, a


class SetParametersM(object):

    def __init__(self, tab1, parametry, fun):
        self.parametry = parametry
        self.fun = fun

        # naturalna śmierć
        self.nat_death = LabelFrame(tab1, text="naturalna śmierć")  # ramka

        self.label_t = Label(self.nat_death, text='t')
        self.label_t.grid(row=0, column=1, padx=10, pady=2)

        self.t_n_d = Entry(self.nat_death)
        self.t_n_d.grid(row=0, column=2, padx=10, pady=2)
        self.t_n_d.config(width=10)
        self.t_n_d.insert(0, parametry[0])

        self.label_a = Label(self.nat_death, text='a')
        self.label_a.grid(row=1, column=1, padx=10, pady=2)

        self.a_n_d = Entry(self.nat_death)
        self.a_n_d.grid(row=1, column=2, padx=10, pady=2)
        self.a_n_d.config(width=10)
        self.a_n_d.insert(0, parametry[1])

        self.label_n = Label(self.nat_death, text='n')
        self.label_n.grid(row=2, column=1, padx=10, pady=2)

        self.n_n_d = Entry(self.nat_death)
        self.n_n_d.grid(row=2, column=2, padx=10, pady=2)
        self.n_n_d.config(width=10)
        self.n_n_d.insert(0, parametry[2])

        self.var_nat_death = IntVar()
        self.check_n_d = Checkbutton(self.nat_death, text="włączone", variable=self.var_nat_death, width=6,
                                     command=self.on_select)
        if self.fun[0] == 1:
            self.check_n_d.select()
        else:
            self.check_n_d.deselect()
        self.check_n_d.grid(row=0, column=3, padx=10, pady=10, rowspan=3)
        self.nat_death.grid(row=0, column=0, rowspan=3, columnspan=1, padx=10, pady=2)

        # rozmnazanie
        self.repr = LabelFrame(tab1, text="rozmnazanie")  # ramka

        self.label_c = Label(self.repr, text='c')
        self.label_c.grid(row=0, column=1, padx=10, pady=2)

        self.c_repr = Entry(self.repr)
        self.c_repr.grid(row=0, column=2, padx=10, pady=2)
        self.c_repr.config(width=10)
        self.c_repr.insert(0, parametry[3])

        self.var_repr = IntVar()  # wartość do checkbuttona
        self.check_repr = Checkbutton(self.repr, text="włączone", variable=self.var_repr, width=6,
                                      command=self.on_select)
        if self.fun[1] == 1:
            self.check_repr.select()
        else:
            self.check_repr.deselect()
        self.check_repr.grid(row=0, column=3, padx=10, pady=2, rowspan=1)
        self.repr.grid(row=0, column=1, rowspan=1, columnspan=1, padx=2, pady=2)

        # kolejna mutacja
        self.mut2 = LabelFrame(tab1, text="kolejna mutacja")  # ramka

        self.label_a2 = Label(self.mut2, text='a')
        self.label_a2.grid(row=0, column=1, padx=10, pady=5)

        self.a2_mut = Entry(self.mut2)
        self.a2_mut.grid(row=0, column=2, padx=10, pady=5)
        self.a2_mut.config(width=10)
        self.a2_mut.insert(0, parametry[6])

        self.var_mut2 = IntVar()
        self.check_mut2 = Checkbutton(self.mut2, text="włączone", variable=self.var_mut2, width=6,
                                      command=self.on_select)
        if self.fun[9] == 1:
            self.check_mut2.select()
        else:
            self.check_mut2.deselect()
        self.check_mut2.grid(row=0, column=3, padx=10, pady=3, rowspan=1)
        self.mut2.grid(row=5, column=0, rowspan=1, columnspan=1, padx=10, pady=0)

        # transformacja
        self.mut = LabelFrame(tab1, text="transformacja nowotworowa")  # ramka

        self.label_a2 = Label(self.mut, text='a')
        self.label_a2.grid(row=0, column=1, padx=10, pady=2)

        self.a_mut = Entry(self.mut)
        self.a_mut.grid(row=0, column=2, padx=10, pady=2)
        self.a_mut.config(width=10)
        self.a_mut.insert(0, parametry[4])

        self.label_n2 = Label(self.mut, text='n')
        self.label_n2.grid(row=1, column=1, padx=10, pady=2)

        self.n_mut = Entry(self.mut)
        self.n_mut.grid(row=1, column=2, padx=10, pady=2)
        self.n_mut.config(width=10)
        self.n_mut.insert(0, parametry[5])

        self.var_mut = IntVar()  # wartość do checkbuttona
        self.check_mut = Checkbutton(self.mut, text="włączone", variable=self.var_mut, width=6,
                                     command=self.on_select)
        if self.fun[2] == 1:
            self.check_mut.select()
        else:
            self.check_mut.deselect()
        self.check_mut.grid(row=0, column=3, padx=10, pady=2, rowspan=2)
        self.mut.grid(row=3, column=0, rowspan=2, columnspan=1, padx=10, pady=7)

        # pozostałe efekty
        self.rest = LabelFrame(tab1, text="pozostałe efekty")  # ramka

        self.var_dam = IntVar()
        self.check_dam = Checkbutton(self.rest, text="uszkodzenie spontaniczne", variable=self.var_dam)
        if self.fun[3] == 1:
            self.check_dam.select()
        else:
            self.check_dam.deselect()
        self.check_dam.grid(row=0, column=0, padx=20, pady=1, sticky='w')

        self.var_rep = IntVar()
        self.check_rep = Checkbutton(self.rest, text="naprawa", variable=self.var_rep)
        if self.fun[4] == 1:
            self.check_rep.select()
        else:
            self.check_rep.deselect()
        self.check_rep.grid(row=1, column=0, padx=20, pady=1, sticky='w')

        self.var_rad = IntVar()  # śmierć od radiacji
        self.check_rad = Checkbutton(self.rest, text="śmierć radiacyjna", variable=self.var_rad)
        if self.fun[5] == 1:
            self.check_rad.select()
        else:
            self.check_rad.deselect()
        self.check_rad.grid(row=2, column=0, padx=20, pady=1, sticky='w')

        self.var_damr = IntVar()
        self.check_damr = Checkbutton(self.rest, text="uszkodzenie radiacyjne", variable=self.var_damr)
        if self.fun[6] == 1:
            self.check_damr.select()
        else:
            self.check_damr.deselect()
        self.check_damr.grid(row=3, column=0, padx=20, pady=1, sticky='w')

        self.var_by = IntVar()
        self.check_by = Checkbutton(self.rest, text="efekt sąsiedztwa", variable=self.var_by)
        if self.fun[7] == 1:
            self.check_by.select()
        else:
            self.check_by.deselect()
        self.check_by.grid(row=4, column=0, padx=20, pady=1, rowspan=1, sticky='w')

        self.var_ad = IntVar()
        self.check_ad = Checkbutton(self.rest, text="odpowiedź adaptacyjna", variable=self.var_ad)
        if self.fun[8] == 1:
            self.check_ad.select()
        else:
            self.check_ad.deselect()
        self.check_ad.grid(row=5, column=0, padx=20, pady=1, rowspan=1, sticky='w')

        self.rest.grid(row=2, column=1, rowspan=6, padx=2, pady=0, sticky='n')

    def on_select(self):
        if self.var_nat_death.get():
            self.a_n_d.config(state='normal')
            self.n_n_d.config(state='normal')
            self.t_n_d.config(state='normal')
        else:
            self.a_n_d.config(state='disabled')
            self.n_n_d.config(state='disabled')
            self.t_n_d.config(state='disabled')

        if self.var_repr.get():
            self.c_repr.config(state='normal')
        else:
            self.c_repr.config(state='disabled')

        if self.var_mut.get():
            self.a_mut.config(state='normal')
            self.n_mut.config(state='normal')
        else:
            self.a_mut.config(state='disabled')
            self.n_mut.config(state='disabled')

        if self.var_mut2.get():
            self.a2_mut.config(state='normal')
        else:
            self.a2_mut.config(state='disabled')

    def reset(self, parametry):
        self.check_n_d.select()
        self.a_n_d.config(state='normal')
        self.n_n_d.config(state='normal')
        self.t_n_d.config(state='normal')
        self.check_repr.select()
        self.c_repr.config(state='normal')
        self.check_mut.select()
        self.a_mut.config(state='normal')
        self.n_mut.config(state='normal')
        self.check_mut2.select()
        self.a2_mut.config(state='normal')

        self.check_dam.select()
        self.check_rep.select()
        self.check_rad.select()
        self.check_damr.select()
        self.check_by.select()
        self.check_ad.select()

        self.t_n_d.delete(0, END)
        self.t_n_d.insert(0, parametry[0])
        self.a_n_d.delete(0, END)
        self.a_n_d.insert(0, parametry[1])
        self.n_n_d.delete(0, END)
        self.n_n_d.insert(0, parametry[2])
        self.c_repr.delete(0, END)
        self.c_repr.insert(0, parametry[3])
        self.a_mut.delete(0, END)
        self.a_mut.insert(0, parametry[4])
        self.n_mut.delete(0, END)
        self.n_mut.insert(0, parametry[5])
        self.a2_mut.delete(0, END)
        self.a2_mut.insert(0, parametry[6])

    def get_data(self):
        try:
            self.parametry[0] = float(self.t_n_d.get())
            self.parametry[1] = float(self.a_n_d.get())
            self.parametry[2] = float(self.n_n_d.get())
            self.parametry[3] = float(self.c_repr.get())
            self.parametry[4] = float(self.a_mut.get())
            self.parametry[5] = float(self.n_mut.get())
            self.parametry[6] = float(self.a2_mut.get())

        except ValueError:
            messagebox.showinfo("uwaga", "Błędnie podany parametr - niepoprawny znak")

        a = [self.var_nat_death.get(), self.var_repr.get(), self.var_mut.get(), self.var_dam.get(),
             self.var_rep.get(), self.var_rad.get(), self.var_damr.get(), self.var_by.get(),
             self.var_ad.get(), self.var_mut2.get()]
        return self.parametry, a


class SetParametersC(object):

    def __init__(self, tab1, parametry, fun):
        self.parametry = parametry
        self.fun = fun

        # naturalna śmierć
        self.nat_death = LabelFrame(tab1, text="naturalna śmierć")  # ramka

        self.label_d = Label(self.nat_death, text='c')
        self.label_d.grid(row=0, column=1, padx=10, pady=2)

        self.t_n_d = Entry(self.nat_death)
        self.t_n_d.grid(row=0, column=2, padx=10, pady=2)
        self.t_n_d.config(width=10)
        self.t_n_d.insert(0, parametry[0])

        self.var_nat_death = IntVar()
        self.check_n_d = Checkbutton(self.nat_death, text="włączone", variable=self.var_nat_death, width=6,
                                     command=self.on_select)
        if self.fun[0] == 1:
            self.check_n_d.select()
        else:
            self.check_n_d.deselect()
        self.check_n_d.grid(row=0, column=3, padx=10, pady=2, rowspan=1)
        self.nat_death.grid(row=0, column=0, rowspan=1, columnspan=1, padx=5, pady=5)

        # rozmnazanie
        self.repr = LabelFrame(tab1, text="rozmnazanie")  # ramka

        self.label_c = Label(self.repr, text='c')
        self.label_c.grid(row=0, column=1, padx=10, pady=2)

        self.c_repr = Entry(self.repr)
        self.c_repr.grid(row=0, column=2, padx=10, pady=2)
        self.c_repr.config(width=10)
        self.c_repr.insert(0, parametry[1])

        self.var_repr = IntVar()  # wartość do checkbuttona
        self.check_repr = Checkbutton(self.repr, text="włączone", variable=self.var_repr, width=6,
                                      command=self.on_select)
        if self.fun[1] == 1:
            self.check_repr.select()
        else:
            self.check_repr.deselect()
        self.check_repr.grid(row=0, column=3, padx=10, pady=2, rowspan=1)
        self.repr.grid(row=2, column=0, rowspan=1, columnspan=1, padx=5, pady=5)

        # radioczułość
        self.rad = LabelFrame(tab1, text="radioczułość")  # ramka

        self.label_c = Label(self.rad, text='c')
        self.label_c.grid(row=0, column=1, padx=10, pady=2)

        self.c_rad = Entry(self.rad)
        self.c_rad.grid(row=0, column=2, padx=10, pady=2)
        self.c_rad.config(width=10)
        self.c_rad.insert(0, parametry[2])

        self.var_rad = IntVar()  # wartość do checkbuttona
        self.check_rad = Checkbutton(self.rad, text="włączone", variable=self.var_rad, width=6, command=self.on_select)
        if self.fun[2] == 1:
            self.check_rad.select()
        else:
            self.check_rad.deselect()
        self.check_rad.grid(row=0, column=3, padx=10, pady=2, rowspan=1)
        self.rad.grid(row=3, column=0, rowspan=1, columnspan=1, padx=5, pady=5)

        # pozostałe efekty
        self.rest = LabelFrame(tab1, text="pozostałe efekty")

        self.var_rad2 = IntVar()  # śmierć od radiacji
        self.check_rad2 = Checkbutton(self.rest, text="śmierć radiacyjna", variable=self.var_rad2)
        if self.fun[3] == 1:
            self.check_rad2.select()
        else:
            self.check_rad2.deselect()
        self.check_rad2.grid(row=2, column=0, padx=10, pady=3, sticky='w')

        self.var_by = IntVar()
        self.check_by = Checkbutton(self.rest, text="efekt sąsiedztwa", variable=self.var_by)
        if self.fun[4] == 1:
            self.check_by.select()
        else:
            self.check_by.deselect()
        self.check_by.grid(row=4, column=0, padx=10, pady=3, sticky='w')

        self.rest.grid(row=0, column=1, rowspan=3, padx=10, pady=5, sticky='n')

    def on_select(self):
        if self.var_nat_death.get():
            self.t_n_d.config(state='normal')
        else:
            self.t_n_d.config(state='disabled')

        if self.var_repr.get():
            self.c_repr.config(state='normal')
        else:
            self.c_repr.config(state='disabled')

        if self.var_rad.get():
            self.c_rad.config(state='normal')
        else:
            self.c_rad.config(state='disabled')

    def reset(self, parametry):

        self.check_n_d.select()
        self.t_n_d.config(state='normal')
        self.check_repr.select()
        self.c_repr.config(state='normal')
        self.check_rad.select()
        self.c_rad.config(state='normal')

        self.check_rad2.select()
        self.check_by.select()

        self.t_n_d.delete(0, END)
        self.t_n_d.insert(0, parametry[0])
        self.c_repr.delete(0, END)
        self.c_repr.insert(0, parametry[1])
        self.c_rad.delete(0, END)
        self.c_rad.insert(0, parametry[2])

    def get_data(self):
        try:
            self.parametry[0] = float(self.t_n_d.get())
            self.parametry[1] = float(self.c_repr.get())
            self.parametry[2] = float(self.c_rad.get())
        except ValueError:
            messagebox.showinfo("uwaga", "Błędnie podany parametr - niepoprawny znak")

        a = [self.var_nat_death.get(), self.var_repr.get(), self.var_rad.get(), self.var_rad2.get(), self.var_by.get()]
        return self.parametry, a


class SetParametersW(object):

    def __init__(self, tab1, parametry):
        self.parametry = parametry

        # trafienie
        self.hit = LabelFrame(tab1, text="trafienie")  # ramka

        self.label_t = Label(self.hit, text='t')
        self.label_t.grid(row=0, column=1, padx=10, pady=2)

        self.t_h = Entry(self.hit)
        self.t_h.grid(row=0, column=2, padx=10, pady=2)
        self.t_h.config(width=15)
        self.t_h.insert(0, parametry[0])

        self.hit.grid(row=0, column=0, rowspan=1, columnspan=1, padx=10, pady=5)

        # spontaniczne uszkodzenie
        self.damage = LabelFrame(tab1, text="spontaniczne uszkodzenie")  # ramka

        self.label_t2 = Label(self.damage, text='t')
        self.label_t2.grid(row=0, column=1, padx=10, pady=2)

        self.t_d = Entry(self.damage)
        self.t_d.grid(row=0, column=2, padx=10, pady=2)
        self.t_d.config(width=15)
        self.t_d.insert(0, parametry[1])

        self.label_a = Label(self.damage, text='a')
        self.label_a.grid(row=1, column=1, padx=10, pady=2)

        self.a_d = Entry(self.damage)
        self.a_d.grid(row=1, column=2, padx=10, pady=2)
        self.a_d.config(width=15)
        self.a_d.insert(0, parametry[2])

        self.label_n = Label(self.damage, text='n')
        self.label_n.grid(row=2, column=1, padx=10, pady=2)

        self.n_d = Entry(self.damage)
        self.n_d.grid(row=2, column=2, padx=10, pady=2)
        self.n_d.config(width=15)
        self.n_d.insert(0, parametry[3])

        self.damage.grid(row=1, column=0, rowspan=3, columnspan=1, padx=5, pady=5)

        # naprawa
        self.repair = LabelFrame(tab1, text="naprawa")  # ramka

        self.label_q = Label(self.repair, text='q')
        self.label_q.grid(row=0, column=1, padx=10, pady=2)

        self.q_n = Entry(self.repair)
        self.q_n.grid(row=0, column=2, padx=10, pady=2)
        self.q_n.config(width=15)
        self.q_n.insert(0, parametry[4])

        self.label_a_n = Label(self.repair, text='a')
        self.label_a_n.grid(row=1, column=1, padx=10, pady=2)

        self.a_n = Entry(self.repair)
        self.a_n.grid(row=1, column=2, padx=10, pady=2)
        self.a_n.config(width=15)
        self.a_n.insert(0, parametry[5])

        self.label_n = Label(self.repair, text='n')
        self.label_n.grid(row=2, column=1, padx=10, pady=2)

        self.n_n = Entry(self.repair)
        self.n_n.grid(row=2, column=2, padx=10, pady=2)
        self.n_n.config(width=15)
        self.n_n.insert(0, parametry[6])

        self.repair.grid(row=1, column=1, rowspan=3, columnspan=1, padx=5, pady=5)

        # uszkodzenie radiacją
        self.rad = LabelFrame(tab1, text="uszkodzenie radiacją")  # ramka

        self.label_rad = Label(self.rad, text='c')
        self.label_rad.grid(row=0, column=1, padx=10, pady=2)

        self.c_rad = Entry(self.rad)
        self.c_rad.grid(row=0, column=2, padx=10, pady=2)
        self.c_rad.config(width=15)
        self.c_rad.insert(0, parametry[7])

        self.rad.grid(row=0, column=1, rowspan=1, columnspan=1, padx=5, pady=5)

        # transformacja/kolejna mutacja
        self.death = LabelFrame(tab1, text="śmierć od radiacji")  # ramka

        self.label_death = Label(self.death, text='c')
        self.label_death.grid(row=0, column=1, padx=10, pady=2)

        self.a_death = Entry(self.death)
        self.a_death.grid(row=0, column=2, padx=10, pady=2)
        self.a_death.config(width=15)
        self.a_death.insert(0, parametry[8])

        self.death.grid(row=4, column=0, rowspan=1, columnspan=1, padx=5, pady=5)

    def reset(self, parametry):
        self.t_h.delete(0, END)
        self.t_h.insert(0, parametry[0])
        self.t_d.delete(0, END)
        self.t_d.insert(0, parametry[1])
        self.a_d.delete(0, END)
        self.a_d.insert(0, parametry[2])
        self.n_d.delete(0, END)
        self.n_d.insert(0, parametry[3])
        self.q_n.delete(0, END)
        self.q_n.insert(0, parametry[4])
        self.a_n.delete(0, END)
        self.a_n.insert(0, parametry[5])
        self.n_n.delete(0, END)
        self.n_n.insert(0, parametry[6])
        self.c_rad.delete(0, END)
        self.c_rad.insert(0, parametry[7])
        self.a_death.delete(0, END)
        self.a_death.insert(0, parametry[8])

    def get_data(self):
        try:
            self.parametry[0] = float(self.t_h.get())
            self.parametry[1] = float(self.t_d.get())
            self.parametry[2] = float(self.a_d.get())
            self.parametry[3] = float(self.n_d.get())
            self.parametry[4] = float(self.q_n.get())
            self.parametry[5] = float(self.a_n.get())
            self.parametry[6] = float(self.n_n.get())
            self.parametry[7] = float(self.c_rad.get())
            self.parametry[8] = float(self.a_death.get())

        except ValueError:
            messagebox.showinfo("uwaga", "Błędnie podany parametr - niepoprawny znak")

        return self.parametry


class SetParametersBA(object):

    def __init__(self, tab1, parametry, parametry1):
        self.parametry = parametry
        self.parametry1 = parametry1

        # sąsiedztwo
        self.b_a = LabelFrame(tab1, text="efekt sąsiedztwa")  # ramka

        self.label_a = Label(self.b_a, text='a')
        self.label_a.grid(row=0, column=1, padx=10, pady=4)

        self.a_b_a = Entry(self.b_a)
        self.a_b_a.grid(row=0, column=2, padx=15, pady=4)
        self.a_b_a.config(width=10)
        self.a_b_a.insert(0, parametry[0])

        self.label_Mw = Label(self.b_a, text='Mw')
        self.label_Mw.grid(row=1, column=1, padx=10, pady=4)

        self.Mw_b_a = Entry(self.b_a)
        self.Mw_b_a.grid(row=1, column=2, padx=15, pady=4)
        self.Mw_b_a.config(width=10)
        self.Mw_b_a.insert(0, parametry[1])

        self.label_Ma = Label(self.b_a, text='M alfa')
        self.label_Ma.grid(row=2, column=1, padx=10, pady=4)

        self.Ma_b_a = Entry(self.b_a)
        self.Ma_b_a.grid(row=2, column=2, padx=15, pady=4)
        self.Ma_b_a.config(width=10)
        self.Ma_b_a.insert(0, parametry[2])

        self.label_Mb = Label(self.b_a, text='M beta')
        self.label_Mb.grid(row=3, column=1, padx=10, pady=4)

        self.Mb_b_a = Entry(self.b_a)
        self.Mb_b_a.grid(row=3, column=2, padx=15, pady=4)
        self.Mb_b_a.config(width=10)
        self.Mb_b_a.insert(0, parametry[3])

        self.label_Gw = Label(self.b_a, text='Gw')
        self.label_Gw.grid(row=4, column=1, padx=10, pady=4)

        self.Gw_b_a = Entry(self.b_a)
        self.Gw_b_a.grid(row=4, column=2, padx=15, pady=4)
        self.Gw_b_a.config(width=10)
        self.Gw_b_a.insert(0, parametry[4])

        self.label_Ga = Label(self.b_a, text='G alfa')
        self.label_Ga.grid(row=5, column=1, padx=10, pady=4)

        self.Ga_b_a = Entry(self.b_a)
        self.Ga_b_a.grid(row=5, column=2, padx=15, pady=4)
        self.Ga_b_a.config(width=10)
        self.Ga_b_a.insert(0, parametry[5])

        self.label_Gb = Label(self.b_a, text='G beta')
        self.label_Gb.grid(row=6, column=1, padx=10, pady=4)

        self.Gb_b_a = Entry(self.b_a)
        self.Gb_b_a.grid(row=6, column=2, padx=15, pady=4)
        self.Gb_b_a.config(width=10)
        self.Gb_b_a.insert(0, parametry[6])

        self.b_a.grid(row=0, column=0, rowspan=7, columnspan=2, padx=10, pady=5)

        # sąsiedztwo
        self.b_a2 = LabelFrame(tab1, text="efekt sąsiedztwa")  # ramka

        self.label_MDP = Label(self.b_a2, text='MDP')
        self.label_MDP.grid(row=1, column=1, padx=15, pady=2)

        self.MDP_b_a = Entry(self.b_a2)
        self.MDP_b_a.grid(row=1, column=2, padx=10, pady=2)
        self.MDP_b_a.config(width=10)
        self.MDP_b_a.insert(0, parametry[8])

        self.label_GJP = Label(self.b_a2, text='GJP')
        self.label_GJP.grid(row=2, column=1, padx=10, pady=2)

        self.GJP_b_a = Entry(self.b_a2)
        self.GJP_b_a.grid(row=2, column=2, padx=15, pady=2)
        self.GJP_b_a.config(width=10)
        self.GJP_b_a.insert(0, parametry[9])

        self.label_t = Label(self.b_a2, text='t')
        self.label_t.grid(row=3, column=1, padx=10, pady=2)

        self.t_b_a = Entry(self.b_a2)
        self.t_b_a.grid(row=3, column=2, padx=15, pady=2)
        self.t_b_a.config(width=10)
        self.t_b_a.insert(0, parametry[10])

        self.b_a2.grid(row=0, column=2, rowspan=3, columnspan=2, padx=10, pady=5)

        # adapt
        self.adapt = LabelFrame(tab1, text="odp adapt")  # ramka

        self.label_a1 = Label(self.adapt, text='a1')
        self.label_a1.grid(row=0, column=1, padx=30, pady=2)

        self.a1 = Entry(self.adapt)
        self.a1.grid(row=0, column=2, padx=15, pady=2)
        self.a1.config(width=10)
        self.a1.insert(0, parametry1[0])

        self.label_a2 = Label(self.adapt, text='a2')
        self.label_a2.grid(row=1, column=1, padx=30, pady=2)

        self.a2 = Entry(self.adapt)
        self.a2.grid(row=1, column=2, padx=15, pady=2)
        self.a2.config(width=10)
        self.a2.insert(0, parametry1[1])

        self.label_a3 = Label(self.adapt, text='a3')
        self.label_a3.grid(row=2, column=1, padx=30, pady=2)

        self.a3 = Entry(self.adapt)
        self.a3.grid(row=2, column=2, padx=15, pady=2)
        self.a3.config(width=10)
        self.a3.insert(0, parametry1[2])

        self.adapt.grid(row=4, column=2, rowspan=3, columnspan=2, padx=10, pady=5)

    def reset(self, parametry, parametry1):

        self.a_b_a.delete(0, END)
        self.a_b_a.insert(0, parametry[0])
        self.Mw_b_a.delete(0, END)
        self.Mw_b_a.insert(0, parametry[1])
        self.Ma_b_a.delete(0, END)
        self.Ma_b_a.insert(0, parametry[2])
        self.Mb_b_a.delete(0, END)
        self.Mb_b_a.insert(0, parametry[3])
        self.Gw_b_a.delete(0, END)
        self.Gw_b_a.insert(0, parametry[4])
        self.Ga_b_a.delete(0, END)
        self.Ga_b_a.insert(0, parametry[5])
        self.Gb_b_a.delete(0, END)
        self.Gb_b_a.insert(0, parametry[6])

        self.MDP_b_a.delete(0, END)
        self.MDP_b_a.insert(0, parametry[8])
        self.GJP_b_a.delete(0, END)
        self.GJP_b_a.insert(0, parametry[9])
        self.t_b_a.delete(0, END)
        self.t_b_a.insert(0, parametry[10])

        self.a1.delete(0, END)
        self.a1.insert(0, parametry1[0])
        self.a2.delete(0, END)
        self.a2.insert(0, parametry1[1])
        self.a3.delete(0, END)
        self.a3.insert(0, parametry1[2])

    def get_data(self):
        try:
            self.parametry[0] = float(self.a_b_a.get())
            self.parametry[1] = float(self.Mw_b_a.get())
            self.parametry[2] = float(self.Ma_b_a.get())
            self.parametry[3] = float(self.Mb_b_a.get())
            self.parametry[4] = float(self.Gw_b_a.get())
            self.parametry[5] = float(self.Ga_b_a.get())
            self.parametry[6] = float(self.Gb_b_a.get())
            self.parametry[8] = float(self.MDP_b_a.get())
            self.parametry[9] = float(self.GJP_b_a.get())
            self.parametry[10] = float(self.t_b_a.get())

            self.parametry1[0] = float(self.a1.get())
            self.parametry1[1] = float(self.a2.get())
            self.parametry1[2] = float(self.a3.get())

        except ValueError:
            messagebox.showinfo("uwaga", "Błędnie podany parametr - niepoprawny znak")

        return self.parametry, self.parametry1
