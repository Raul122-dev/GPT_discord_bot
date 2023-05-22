import discord
from discord import ui
from discord.ui import Button, View

class MyButtons(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="Regenerar", custom_id="button1", style=discord.ButtonStyle.green))
        self.add_item(Button(label="Usar otro modelo", custom_id="button2", style=discord.ButtonStyle.red))

    # @ui.button(label="Regenerar", custom_id="button1", style=discord.ButtonStyle.green)
    # async def button_1(self, button: Button, interaction: discord.Interaction):
    #     await interaction.response.send_message("Haz presionado el Botón regerar.", ephemeral=True)

    # @ui.button(label="Usar otro modelo", custom_id="button2", style=discord.ButtonStyle.red)
    # async def button_2(self, button: Button, interaction: discord.Interaction):
    #     await interaction.response.send_message("Haz presionado el Botón otro modelo.", ephemeral=True)
