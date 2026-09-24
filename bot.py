import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
from datetime import timedelta

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=".",
    intents=intents
)

SPECIAL_ROLE_ID = 1551011482362314812

TRAINER_ROLE_ID = 1550955735364403311
GMOD_ROLE_ID = 1552438260708544634
MODERATOR_ROLE_ID = 1550944205910843503
ADMIN_ROLE_ID = 1550944006039666829
CO_OWNER_ROLE_ID = 1552416873612841110
CHOSEN_ROLE_ID = 1550955220521984030

with open("warnings.json", "r") as f:
    warnings = json.load(f)

with open("role_backup.json", "r") as f:
    role_backup = json.load(f)

def save_warnings():
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)

def has_role(member, role_ids):
    return any(role.id in role_ids for role in member.roles)

def save_role_backup():
    with open("role_backup.json", "w") as f:
        json.dump(role_backup, f, indent=4)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    print(f"Message received: {message.content}")
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def ورن(ctx, member: discord.Member, *, reason="No reason provided"):

    allowed_roles = [
        TRAINER_ROLE_ID,
        GMOD_ROLE_ID,
        MODERATOR_ROLE_ID,
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم الأمر ده.")
        return

    user_id = str(member.id)

    if user_id not in warnings:
        warnings[user_id] = []

    warnings[user_id].append(reason)
    save_warnings()

    count = len(warnings[user_id])

    if count >= 3:
        duration = discord.utils.utcnow() + timedelta(hours=1)

        await member.timeout(
            duration,
            reason="Reached 3 warnings"
        )

        await ctx.send(
            f"⏱️ {member.mention} وصل لـ 3 تحذيرات واتعمله تايم أوت لمدة ساعة."
        )

    await ctx.send(
        f"⚠️ {member.mention} اتعمله تحذير.\n"
        f"السبب: {reason}\n"
        f"التحذيرات: {count}/3"
    )

@bot.command()
async def تايم(ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):

    allowed_roles = [
        GMOD_ROLE_ID,
        MODERATOR_ROLE_ID,
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم الأمر ده.")
        return

    duration = discord.utils.utcnow() + timedelta(minutes=minutes)

    await member.timeout(
        duration,
        reason=reason
    )

    await ctx.send(
        f"⏱️ {member.mention} اتعمله تايم أوت لمدة **{minutes} دقيقة**.\n"
        f"السبب: {reason}"
    )

@bot.command()
async def بان(ctx, member: discord.Member, *, reason="No reason provided"):

    allowed_roles = [
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم أمر البان.")
        return

    await member.ban(reason=reason)

    await ctx.send(
        f"🔨 {member.mention} اتعمله بان.\n"
        f"السبب: {reason}"
    )

@bot.command()
async def كيك(ctx, member: discord.Member, *, reason="No reason provided"):

    allowed_roles = [
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم الأمر ده.")
        return

    await member.kick(reason=reason)

    await ctx.send(
        f"👢 {member.mention} اتعمله كيك.\n"
        f"السبب: {reason}"
    )

@bot.command()
async def مسح(ctx, amount: int):

    allowed_roles = [
        GMOD_ROLE_ID,
        MODERATOR_ROLE_ID,
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم أمر المسح.")
        return

    if amount <= 0:
        await ctx.send("❌ اكتب عدد رسائل أكبر من 0.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)

    msg = await ctx.send(
        f"🧹 تم مسح **{len(deleted) - 1}** رسالة."
    )

    await msg.delete(delay=3)

@bot.command()
async def انبان(ctx, user_id: int):

    allowed_roles = [
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم أمر الـ Unban.")
        return

    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)

        await ctx.send(
            f"✅ تم فك البان عن **{user}**."
        )

    except discord.NotFound:
        await ctx.send("❌ المستخدم مش موجود أو مش متبند.")

    except discord.Forbidden:
        await ctx.send("❌ البوت معندوش صلاحية يعمل Unban.")

@bot.command()
async def انورن(ctx, member: discord.Member):

    allowed_roles = [
        TRAINER_ROLE_ID,
        GMOD_ROLE_ID,
        MODERATOR_ROLE_ID,
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم الأمر ده.")
        return

    user_id = str(member.id)

    if user_id not in warnings or len(warnings[user_id]) == 0:
        await ctx.send(
            f"❌ {member.mention} معندوش تحذيرات."
        )
        return

    removed_reason = warnings[user_id].pop()
    save_warnings()

    await ctx.send(
        f"✅ تم إزالة آخر تحذير من {member.mention}.\n"
        f"السبب: {removed_reason}\n"
        f"التحذيرات: {len(warnings[user_id])}/3"
    )

@bot.command()
async def انتايم(ctx, member: discord.Member):

    allowed_roles = [
        GMOD_ROLE_ID,
        MODERATOR_ROLE_ID,
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم الأمر ده.")
        return

    await member.timeout(
        None,
        reason=f"Untimeout by {ctx.author}"
    )

    await ctx.send(
        f"✅ {member.mention} اتشال منه التايم أوت."
    )

SPECIAL_ROLE_ID = 1551011482362314812
ALLOWED_CATEGORY_ID = 1550987278942343329

@bot.command()
async def لف(ctx, member: discord.Member):

    # الصلاحية: Admin + CO Owner + THE CHOSEN فقط
    allowed_roles = [
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم أمر السجن.")
        return

    user_id = str(member.id)

    # منع تكرار اللف على نفس العضو
    if user_id in role_backup:
        await ctx.send("❌ العضو بالفعل في حالة اللف.")
        return

    # حفظ الرولات القديمة
    role_backup[user_id] = [
        role.id
        for role in member.roles
        if role != ctx.guild.default_role
    ]
    save_role_backup()

    # الحصول على رول السجن
    special_role = ctx.guild.get_role(SPECIAL_ROLE_ID)

    if special_role is None:
        await ctx.send("❌ رول السجن مش موجود.")
        return

    # إزالة كل الرولات القديمة
    old_roles = [
        role
        for role in member.roles
        if role != ctx.guild.default_role
    ]

    if old_roles:
        await member.remove_roles(*old_roles)

    # إعطاء رول السجن
    await member.add_roles(special_role)

    # الحصول على Category السجن
    allowed_category = ctx.guild.get_channel(ALLOWED_CATEGORY_ID)

    if allowed_category is None or not isinstance(
        allowed_category,
        discord.CategoryChannel
    ):
        await ctx.send("❌ الـ Category المحددة مش موجودة.")
        return

    # لو العضو داخل Voice وقت تنفيذ الأمر
    # يخرج تلقائيًا
    if member.voice is not None:
        try:
            await member.move_to(None)
        except discord.Forbidden:
            pass

    # التحكم في كل الـ Categories والـ Channels
    for channel in ctx.guild.channels:

        try:

            # Categories
            if isinstance(channel, discord.CategoryChannel):

                if channel.id == ALLOWED_CATEGORY_ID:

                    await channel.set_permissions(
                        member,
                        view_channel=True
                    )

                else:

                    await channel.set_permissions(
                        member,
                        view_channel=False,
                        send_messages=False,
                        connect=False
                    )

            # Text Channels
            elif isinstance(channel, discord.TextChannel):

                if channel.category_id == ALLOWED_CATEGORY_ID:

                    await channel.set_permissions(
                        member,
                        view_channel=True,
                        send_messages=True
                    )

                else:

                    await channel.set_permissions(
                        member,
                        view_channel=False,
                        send_messages=False
                    )

            # Voice Channels
            elif isinstance(channel, discord.VoiceChannel):

                if channel.category_id == ALLOWED_CATEGORY_ID:

                    await channel.set_permissions(
                        member,
                        view_channel=True,
                        connect=True
                    )

                else:

                    await channel.set_permissions(
                        member,
                        view_channel=False,
                        connect=False
                    )

        except discord.Forbidden:
            pass

    # مسح آخر 15 رسالة للعضو
    try:

        deleted = 0

        async for message in ctx.channel.history(limit=100):

            if message.author.id == member.id:

                try:
                    await message.delete()
                    deleted += 1

                    if deleted >= 15:
                        break

                except discord.NotFound:
                    pass

    except discord.Forbidden:
        pass

    # رسالة التأكيد
    await ctx.send(
        f"🔒 {member.mention} اتعمله لف.\n"
        f"🔐 المسموح له بالكلام: **{allowed_category.name}**\n"
        f"🧹 تم مسح آخر **{deleted}** رسالة للعضو."
    )

# =========================================================
# مراقبة الـ Voice للأعضاء المسجونين
# =========================================================

@bot.event
async def on_voice_state_update(member, before, after):

    user_id = str(member.id)

    # لو العضو مش مسجون
    if user_id not in role_backup:
        return

    # لو العضو دخل Voice
    if after.channel is not None:

        # لو الـ Voice مش داخل Category السجن
        # يخرج تلقائيًا
        if after.channel.category_id != ALLOWED_CATEGORY_ID:

            try:
                await member.move_to(None)
            except discord.Forbidden:
                pass

            return

        # لو دخل Voice السجن
        # يتعمله Server Mute تلقائي
        try:
            if member.voice and not member.voice.server_mute:
                await member.edit(mute=True)
        except discord.Forbidden:
            pass


# =========================================================
# الإفراج
# =========================================================

@bot.command()
async def افراج(ctx, member: discord.Member):

    # الصلاحية: Admin + CO Owner + THE CHOSEN فقط
    allowed_roles = [
        ADMIN_ROLE_ID,
        CO_OWNER_ROLE_ID,
        CHOSEN_ROLE_ID
    ]

    if not has_role(ctx.author, allowed_roles):
        await ctx.send("❌ معندكش صلاحية تستخدم أمر الإفراج.")
        return

    user_id = str(member.id)

    # التأكد إن العضو مسجون
    if user_id not in role_backup:
        await ctx.send("❌ العضو ده مش في حالة اللف.")
        return

    # الحصول على رول السجن
    special_role = ctx.guild.get_role(SPECIAL_ROLE_ID)

    # إزالة رول السجن
    if special_role and special_role in member.roles:
        try:
            await member.remove_roles(special_role)
        except discord.Forbidden:
            pass

    # استرجاع الرولات القديمة
    old_roles = []

    for role_id in role_backup[user_id]:
        role = ctx.guild.get_role(role_id)

        if role:
            old_roles.append(role)

    if old_roles:
        try:
            await member.add_roles(*old_roles)
        except discord.Forbidden:
            pass

    # إزالة كل الـ permissions الخاصة بالعضو
    for channel in ctx.guild.channels:

        try:
            if isinstance(
                channel,
                (
                    discord.CategoryChannel,
                    discord.TextChannel,
                    discord.VoiceChannel
                )
            ):
                await channel.set_permissions(
                    member,
                    overwrite=None
                )

        except discord.Forbidden:
            pass

    # فك الـ Server Mute
    if member.voice is not None:
        try:
            await member.edit(mute=False)
        except discord.Forbidden:
            pass

    # حذف بيانات الحفظ
    del role_backup[user_id]
    save_role_backup()

    await ctx.send(
        f"🔓 {member.mention} اتعمله إفراج.\n"
        f"✅ تم استرجاع الرولات والصلاحيات القديمة."
    )

bot.run(TOKEN)