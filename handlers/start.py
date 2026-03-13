from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from database import get_user, create_user
from game import regen_energy, energy_full_in, get_active_buffs
from keyboards import main_menu_kb, mine_action_kb
from config import TOOLS, ZONES

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    uid = message.from_user.id
    uname = message.from_user.username or ""
    fname = message.from_user.first_name or "Miner"

    ref_id = None
    parts = message.text.split()
    if len(parts) > 1:
        try:
            ref = int(parts[1])
            if ref != uid:
                ref_id = ref
        except ValueError:
            pass

    existing = await get_user(uid)
    if not existing:
        await create_user(uid, uname, fname, ref_id)
        text = (
            f"⛏️ *Selamat Datang di Mining Bot, {fname}!*\n\n"
            f"🎮 Kamu telah bergabung sebagai penambang!\n"
            f"💰 Saldo awal: *200 koin*\n"
            f"⛏️ Alat starter: *Beliung Batu* (Gratis)\n"
            f"📍 Zona awal: *Permukaan*\n\n"
            f"🚀 Mulai mining dan kumpulkan koin sebanyak mungkin!\n"
            f"Gunakan tombol di bawah untuk navigasi."
        )
        if ref_id:
            text += f"\n\n🎁 Kamu bergabung via referral! Bonus *300 koin* dikirim!"
    else:
        user = await regen_energy(existing)
        tool = TOOLS.get(user["current_tool"], TOOLS["stone_pick"])
        zone = ZONES.get(user.get("current_zone", "surface"), ZONES["surface"])
        buffs = get_active_buffs(user)
        buff_txt = ""
        if buffs:
            buff_txt = "\n⚡ *Buff aktif:* " + ", ".join(buffs.keys())

        text = (
            f"👋 *Selamat kembali, {fname}!*\n\n"
            f"💰 Saldo   : `{user['balance']:,}` koin\n"
            f"⚡ Energy  : `{user['energy']}/{user['max_energy']}`\n"
            f"⭐ Level   : `{user['level']}`\n"
            f"🔧 Alat    : {tool['emoji']} {tool['name']}\n"
            f"📍 Zona    : {zone['name']}"
            f"{buff_txt}"
        )

    await message.answer(text, reply_markup=main_menu_kb(), parse_mode="Markdown")


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery):
    uid = callback.from_user.id
    user = await get_user(uid)
    if not user:
        await callback.answer("Ketik /start dulu!")
        return
    tool = TOOLS.get(user["current_tool"], TOOLS["stone_pick"])
    zone = ZONES.get(user.get("current_zone", "surface"), ZONES["surface"])
    text = (
        f"🏠 *Menu Utama*\n\n"
        f"💰 Saldo  : `{user['balance']:,}` koin\n"
        f"⚡ Energy : `{user['energy']}/{user['max_energy']}`\n"
        f"⭐ Level  : `{user['level']}`\n"
        f"🔧 Alat   : {tool['emoji']} {tool['name']}\n"
        f"📍 Zona   : {zone['name']}"
    )
    await callback.message.edit_text(text, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer()
