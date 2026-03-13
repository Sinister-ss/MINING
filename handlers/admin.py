"""
🔐 Admin Handler — Khusus Admin, Tidak Terkena Biaya Apapun
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import ADMIN_IDS, TOOLS, ITEMS, ZONES
from database import get_user, update_user, get_all_users, get_total_users, add_balance
from keyboards import admin_kb, back_main_kb

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def admin_only(func):
    """Decorator to restrict handler to admins."""
    async def wrapper(event, *args, **kwargs):
        uid = event.from_user.id if hasattr(event, "from_user") else None
        if uid not in ADMIN_IDS:
            if hasattr(event, "answer"):
                await event.answer("❌ Kamu bukan admin!")
            return
        return await func(event, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ══════════════════════════════════════════════════════════════
# /adminhelp — Panduan lengkap admin
# ══════════════════════════════════════════════════════════════
@router.message(Command("adminhelp"))
async def cmd_adminhelp(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Kamu bukan admin!")
        return

    text = (
        "🔐 *PANEL ADMIN — Mining Bot*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎁 *Keistimewaan Admin:*\n"
        "• Beli alat tanpa biaya koin\n"
        "• Beli item tanpa biaya koin\n"
        "• Buka zona tanpa biaya koin\n"
        "• Semua level requirement diabaikan\n"
        "• Akses semua perintah admin\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📋 *DAFTAR PERINTAH ADMIN:*\n\n"

        "👤 *Manajemen User:*\n"
        "`/admin_info <user_id>` — Lihat info user\n"
        "`/admin_addcoin <user_id> <jumlah>` — Tambah koin\n"
        "`/admin_setlevel <user_id> <level>` — Set level\n"
        "`/admin_setenergy <user_id> <jumlah>` — Set energy\n"
        "`/admin_givetool <user_id> <tool_id>` — Beri alat\n"
        "`/admin_giveitem <user_id> <item_id> <qty>` — Beri item\n"
        "`/admin_givezone <user_id> <zone_id>` — Buka zona\n"
        "`/admin_reset <user_id>` — Reset data user\n\n"

        "📊 *Statistik:*\n"
        "`/admin_stats` — Statistik bot keseluruhan\n"
        "`/admin_users` — Daftar semua user\n\n"

        "📢 *Broadcast:*\n"
        "`/admin_broadcast <pesan>` — Kirim pesan ke semua user\n\n"

        "🎲 *Game Control:*\n"
        "`/admin_tools` — Daftar semua tool_id\n"
        "`/admin_items` — Daftar semua item_id\n"
        "`/admin_zones` — Daftar semua zone_id\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 *Tips:*\n"
        "• Gunakan Shop normal untuk beli tanpa bayar\n"
        "• Admin otomatis terdeteksi dari ADMIN_IDS di .env\n"
        "• Tambah admin di Railway: ADMIN\\_IDS=123456,789012"
    )
    await message.answer(text, parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_stats
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Bukan admin!")
        return
    total = await get_total_users()
    users = await get_all_users()
    total_coins = sum(u["balance"] for u in users)
    total_mined = sum(u["total_mined"] for u in users)
    top = sorted(users, key=lambda x: x["total_mined"], reverse=True)[:3]
    top_txt = "\n".join(
        f"  {i+1}. {u.get('username') or u.get('first_name','?')} — {u['total_mined']:,}"
        for i, u in enumerate(top)
    )
    text = (
        f"📊 *Statistik Bot*\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"👥 Total User    : `{total}`\n"
        f"💰 Total Koin    : `{total_coins:,}`\n"
        f"⛏️ Total Mined   : `{total_mined:,}`\n\n"
        f"🏆 Top 3 Miner:\n{top_txt}"
    )
    await message.answer(text, parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_info <user_id>
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_info"))
async def cmd_admin_info(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Bukan admin!")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Penggunaan: `/admin_info <user_id>`", parse_mode="Markdown")
        return
    try:
        uid = int(parts[1])
    except ValueError:
        await message.answer("❌ user_id harus angka!")
        return
    user = await get_user(uid)
    if not user:
        await message.answer(f"❌ User `{uid}` tidak ditemukan.")
        return
    text = (
        f"👤 *Info User `{uid}`*\n"
        f"Nama     : {user.get('first_name','-')} @{user.get('username','-')}\n"
        f"Balance  : `{user['balance']:,}`\n"
        f"Total    : `{user['total_mined']:,}`\n"
        f"Mine cnt : `{user['mine_count']}`\n"
        f"Level    : `{user['level']}`\n"
        f"Energy   : `{user['energy']}/{user['max_energy']}`\n"
        f"Alat     : `{user['current_tool']}`\n"
        f"Zona     : `{user.get('current_zone','surface')}`\n"
        f"Streak   : `{user.get('daily_streak',0)}`\n"
        f"Rebirth  : `{user.get('rebirth_count',0)}`"
    )
    await message.answer(text, parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_addcoin <user_id> <amount>
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_addcoin"))
async def cmd_addcoin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Penggunaan: `/admin_addcoin <user_id> <jumlah>`", parse_mode="Markdown")
        return
    try:
        uid, amount = int(parts[1]), int(parts[2])
    except ValueError:
        await message.answer("❌ Format salah!")
        return
    await add_balance(uid, amount, f"Admin grant by {message.from_user.id}")
    await message.answer(f"✅ +`{amount:,}` koin dikirim ke user `{uid}`", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_setlevel <user_id> <level>
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_setlevel"))
async def cmd_setlevel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Penggunaan: `/admin_setlevel <user_id> <level>`", parse_mode="Markdown")
        return
    try:
        uid, lv = int(parts[1]), int(parts[2])
    except ValueError:
        await message.answer("❌ Format salah!")
        return
    await update_user(uid, level=max(1, min(lv, 100)))
    await message.answer(f"✅ Level user `{uid}` di-set ke `{lv}`", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_setenergy <user_id> <amount>
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_setenergy"))
async def cmd_setenergy(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Penggunaan: `/admin_setenergy <user_id> <jumlah>`", parse_mode="Markdown")
        return
    try:
        uid, en = int(parts[1]), int(parts[2])
    except ValueError:
        await message.answer("❌ Format salah!")
        return
    user = await get_user(uid)
    if not user:
        await message.answer("❌ User tidak ditemukan!")
        return
    new_e = min(en, user["max_energy"])
    await update_user(uid, energy=new_e)
    await message.answer(f"✅ Energy user `{uid}` di-set ke `{new_e}`", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_givetool <user_id> <tool_id>
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_givetool"))
async def cmd_givetool(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Penggunaan: `/admin_givetool <user_id> <tool_id>`", parse_mode="Markdown")
        return
    uid = int(parts[1])
    tool_id = parts[2]
    if tool_id not in TOOLS:
        await message.answer(f"❌ tool_id tidak valid. Cek `/admin_tools`", parse_mode="Markdown")
        return
    from game import buy_tool
    ok, msg = await buy_tool(uid, tool_id, admin=True)
    await message.answer(f"✅ {msg}", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_giveitem <user_id> <item_id> [qty]
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_giveitem"))
async def cmd_giveitem(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Penggunaan: `/admin_giveitem <user_id> <item_id> [qty]`", parse_mode="Markdown")
        return
    uid = int(parts[1])
    item_id = parts[2]
    qty = int(parts[3]) if len(parts) > 3 else 1
    if item_id not in ITEMS:
        await message.answer(f"❌ item_id tidak valid. Cek `/admin_items`", parse_mode="Markdown")
        return
    user = await get_user(uid)
    if not user:
        await message.answer("❌ User tidak ditemukan!")
        return
    inv = user["inventory"]
    inv[item_id] = inv.get(item_id, 0) + qty
    await update_user(uid, inventory=inv)
    await message.answer(f"✅ `{qty}x {ITEMS[item_id]['name']}` dikirim ke user `{uid}`", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_givezone <user_id> <zone_id>
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_givezone"))
async def cmd_givezone(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Penggunaan: `/admin_givezone <user_id> <zone_id>`", parse_mode="Markdown")
        return
    uid = int(parts[1])
    zone_id = parts[2]
    from game import unlock_zone
    ok, msg = await unlock_zone(uid, zone_id, admin=True)
    await message.answer(f"{'✅' if ok else '❌'} {msg}", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_reset <user_id>
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_reset"))
async def cmd_reset(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Penggunaan: `/admin_reset <user_id>`", parse_mode="Markdown")
        return
    uid = int(parts[1])
    await update_user(uid,
        balance=200, total_earned=0, total_mined=0, mine_count=0,
        energy=100, max_energy=100, level=1, xp=0,
        current_tool="stone_pick", current_zone="surface",
        owned_tools=["stone_pick"], unlocked_zones=["surface"],
        inventory={}, active_buffs={}, achievements=[],
        daily_streak=0, rebirth_count=0, perm_coin_mult=1.0
    )
    await message.answer(f"✅ User `{uid}` berhasil direset.", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_broadcast <pesan>
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_broadcast"))
async def cmd_broadcast(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    text = message.text.replace("/admin_broadcast", "").strip()
    if not text:
        await message.answer("Penggunaan: `/admin_broadcast <pesan>`", parse_mode="Markdown")
        return
    users = await get_all_users()
    sent = failed = 0
    for u in users:
        try:
            await message.bot.send_message(u["user_id"], f"📢 *Pengumuman:*\n\n{text}", parse_mode="Markdown")
            sent += 1
        except Exception:
            failed += 1
    await message.answer(f"✅ Broadcast selesai!\nTerkirim: `{sent}` | Gagal: `{failed}`", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════
# /admin_tools, /admin_items, /admin_zones
# ══════════════════════════════════════════════════════════════
@router.message(Command("admin_tools"))
async def cmd_admin_tools(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    lines = ["⛏️ *Daftar Tool ID:*\n"]
    for tid, t in TOOLS.items():
        lines.append(f"`{tid}` — {t['emoji']} {t['name']} (Tier {t['tier']})")
    await message.answer("\n".join(lines), parse_mode="Markdown")


@router.message(Command("admin_items"))
async def cmd_admin_items(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    lines = ["🎒 *Daftar Item ID:*\n"]
    for iid, item in ITEMS.items():
        lines.append(f"`{iid}` — {item['emoji']} {item['name']}")
    await message.answer("\n".join(lines), parse_mode="Markdown")


@router.message(Command("admin_zones"))
async def cmd_admin_zones(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    lines = ["🌍 *Daftar Zone ID:*\n"]
    for zid, z in ZONES.items():
        lines.append(f"`{zid}` — {z['name']} (Lv.{z['level_req']})")
    await message.answer("\n".join(lines), parse_mode="Markdown")


@router.message(Command("admin_users"))
async def cmd_admin_users(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌")
        return
    users = await get_all_users()
    lines = [f"👥 *Daftar User ({len(users)}):*\n"]
    for u in users[:20]:
        name = u.get("username") or u.get("first_name", "?")
        lines.append(f"`{u['user_id']}` @{name} Lv.{u['level']} — {u['balance']:,}🪙")
    if len(users) > 20:
        lines.append(f"\n_...dan {len(users)-20} lainnya_")
    await message.answer("\n".join(lines), parse_mode="Markdown")
