from models.GUI_form import Form
from models.GUI_button import Button

class FormMenu(Form):
    def __init__(self, master_surface, x, y, w, h, background_color="Black", border_color="Red", active=False) -> None:
        super().__init__(master_surface, x, y, w, h, background_color, border_color, active)
        
        


        self.button1 = Button(master_surface=self.slave_surface,x=100,y=200,w=200,h=30,background_color="Blue",border_color="Green",on_click=self.on_click_button1,on_click_param="1234",text="menu",font="Arial", font_size=20,font_color="Green" )
        self.button2 = Button(master_surface=self.slave_surface,x=100,y=400,w=200,h=30,background_color="Blue",border_color="Green",on_click=self.on_click_button1,on_click_param="1234",text="menu",font="Arial", font_size=20,font_color="Green" )
        self.button3 = Button(master_surface=self.slave_surface,x=100,y=300,w=200,h=30,background_color="Blue",border_color="Green",on_click=self.on_click_button1,on_click_param="1234",text="menu",font="Arial", font_size=20,font_color="Green" )
        self.list_button = [self.button1, self.button2,self.button3]




    def on_click_button1(self,parametro):
        print("click", parametro) 

    def update(self, list_events):
        
        
        for button in self.list_button:
            button.update(list_events)
    
    def draw(self):
        
        super().draw()

        for button in self.list_button:
            button.draw()