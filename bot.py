import discord
from discord.utils import get

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True  # Habilitar acceso al contenido de los mensajes
intents.members = True  # Habilitar acceso a la lista de miembros

# Nombre del usuario a verificar
TARGET_USER_NAME = "luistamalero"

# Crear el cliente de Discord
client = discord.Client(intents=intents)

# Datos de canciones con imágenes
# INSTRUCCIONES: Reemplaza las URLs con tus propias imágenes
# Opción 1: Sube a Discord → clic derecho → copiar enlace
# Opción 2: Sube a Imgur.com → copia el enlace directo
# Opción 3: Usa imágenes de Spotify/YouTube directamente

CANCIONES = {
    'the_warning': [
        {
            'titulo': 'Disciple',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/TheWarning/disciple.jpg',  # Reemplaza con tu imagen
            'descripcion': 'Cancionsota con riffs intensos'
        },
        {
            'titulo': 'Enter Sandman (Cover)',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/TheWarning/enter.jpg',  # Reemplaza con tu imagen
            'descripcion': 'Su cover de Metallica'
        },
        {
            'titulo': 'Automatic Sun',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/TheWarning/sun.gif',  # Reemplaza con tu imagen
            'descripcion': 'When estas tan drogado que haces automático el sol'
        },
        {
            'titulo': 'Queen of the Murder Scene',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/TheWarning/queen.jpg',  # Reemplaza con tu imagen
            'descripcion': 'Cuchillitos Cuchullitos'
        },
        {
            'titulo': 'Amour',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/TheWarning/amour.gif',  # Reemplaza con tu imagen
            'descripcion': 'Sangra por mí'
        }
    ],
    'humbe': [
        {
            'titulo': 'Fantasmas',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/Humbe/fantasmas.jpg',  # Reemplaza con tu imagen
            'descripcion': ''
        },
        {
            'titulo': 'Astros',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/Humbe/astros.jpg',  # Reemplaza con tu imagen
            'descripcion': ''
        },
        {
            'titulo': 'Patadas de Ahogado',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/Humbe/patadas.jpg',  # Reemplaza con tu imagen
            'descripcion': 'Hueles a vainilla, te quiero <3'
        },
        {
            'titulo': 'Sábanas',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/Humbe/sabanas.png',  # Reemplaza con tu imagen
            'descripcion': '¿Y si aún no estoy listo para amar?'
        },
        {
            'titulo': 'REM',
            'imagen': 'https://raw.githubusercontent.com/LuisCT13/Imagenes-Bot-de-Discord/main/Humbe/rem.jpg',  # Reemplaza con tu imagen
            'descripcion': 'Aún te veo en mis sueños'
        }
    ]
}

class CarruselView(discord.ui.View):
    def __init__(self, artista, canciones):
        super().__init__(timeout=180)  # 3 minutos de timeout
        self.artista = artista
        self.canciones = canciones
        self.indice_actual = 0
        
    def crear_embed(self):
        cancion = self.canciones[self.indice_actual]
        
        embed = discord.Embed(
            title=f"🎵 {cancion['titulo']}",
            description=cancion['descripcion'],
            color=0x9b59b6 if self.artista == 'The Warning' else 0x3498db
        )
        
        embed.set_image(url=cancion['imagen'])
        embed.set_footer(
            text=f"{self.artista} | Canción {self.indice_actual + 1} de {len(self.canciones)}"
        )
        
        return embed
    
    @discord.ui.button(label='◀️ Anterior', style=discord.ButtonStyle.primary)
    async def boton_anterior(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.indice_actual = (self.indice_actual - 1) % len(self.canciones)
        await interaction.response.edit_message(embed=self.crear_embed(), view=self)
    
    @discord.ui.button(label='▶️ Siguiente', style=discord.ButtonStyle.primary)
    async def boton_siguiente(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.indice_actual = (self.indice_actual + 1) % len(self.canciones)
        await interaction.response.edit_message(embed=self.crear_embed(), view=self)
    
    @discord.ui.button(label='❌ Cerrar', style=discord.ButtonStyle.danger)
    async def boton_cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None)
        self.stop()

# Evento cuando el bot está listo
@client.event
async def on_ready():
    print(f'El bot ha sido iniciado para este servidor como: {client.user}')

# Evento cuando se recibe un mensaje
@client.event
async def on_message(msg):
    # Ignorar mensajes del propio bot
    if msg.author == client.user:
        return

    # Verificar si el mensaje menciona a alguien
    if msg.mentions:
        for member in msg.mentions:
            if member.name.lower() == TARGET_USER_NAME.lower():
                await msg.reply("Toy viendo pelis :D, como a las 10pm entro.")

    # Comando para mostrar canciones favoritas
    if msg.content.startswith("!artistas"):
        # Crear embed de selección
        embed_menu = discord.Embed(
            title="🎵 Mis Artistas Favoritos",
            description="Selecciona un artista para ver mis canciones favoritas:",
            color=0xe74c3c
        )
        
        embed_menu.add_field(
            name="⚡ The Warning",
            value="Banda de tres hermanas regiomontanas",
            inline=False
        )
        
        embed_menu.add_field(
            name="🎤 Humbe",
            value="Cantante indie/alternativo con letras que me gustan mucho",
            inline=False
        )
        
        # Crear vista con botones de selección
        class MenuView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)
            
            @discord.ui.button(label='⚡ The Warning', style=discord.ButtonStyle.success)
            async def the_warning_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
                view = CarruselView('The Warning', CANCIONES['the_warning'])
                await interaction.response.edit_message(embed=view.crear_embed(), view=view)
            
            @discord.ui.button(label='🎤 Humbe', style=discord.ButtonStyle.success)
            async def humbe_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
                view = CarruselView('Humbe', CANCIONES['humbe'])
                await interaction.response.edit_message(embed=view.crear_embed(), view=view)
        
        await msg.reply(embed=embed_menu, view=MenuView())

    # Comando para dar permisos de administrador
    if msg.content.startswith("!darAdmin"):
        # Verificar si el autor del mensaje tiene permisos para gestionar roles
        if not msg.author.guild_permissions.manage_roles:
            await msg.reply("❌ No tienes permisos para gestionar roles.")
            return

        # Verificar si se mencionó a un usuario
        if not msg.mentions:
            await msg.reply("❌ Debes mencionar a un usuario.")
            return

        # Obtener el usuario mencionado
        target_member = msg.mentions[0]

        # Buscar el rol de administrador
        admin_role = get(msg.guild.roles, name="Admin Bot")

        # Si el rol no existe, crearlo
        if not admin_role:
            admin_role = await msg.guild.create_role(
                name="Admin Bot",
                permissions=discord.Permissions(administrator=True),
                reason="Rol de administrador creado por el bot."
            )
            await msg.reply(f"✅ Rol de administrador creado: {admin_role.name}")

        # Asignar el rol al usuario mencionado
        await target_member.add_roles(admin_role)
        await msg.reply(f"✅ Rol de administrador asignado a {target_member.mention}.")

# Iniciar el bot
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de ambiente desde .env

# Usar variable de ambiente para el token
client.run(os.getenv('DISCORD_TOKEN'))
