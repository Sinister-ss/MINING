"""
❓ Help Handler
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import back_main_kb

router = Router()


@router.message(F.text == "❓ Bantuan")
@router.message(Command("help"))
async def show_help(message: Message):
    text = (
        "❓ *Panduan Mining Bot*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "⛏️ *CARA MINING:*\n"
        "1. Tekan menu *⛏️ Mining*\n"
        "2. Pilih *Mine!*, *Mine x5*, atau *Mine x10*\n"
        "3. Tiap mining menghabiskan ⚡ Energy\n"
        "4. Energy regen otomatis 1/menit\n\n"

        "🎒 *PERALATAN (Equipment):*\n"
        "• Lihat & ganti alat di *🎒 Equipment*\n"
        "• Beli alat baru di *🏪 Shop → Alat Mining*\n"
        "• Ada 7 Tier alat, dari Gratis hingga Mythical!\n"
        "• Alat lebih mahal = power, speed, & luck lebih tinggi\n\n"

        "🌍 *ZONA MINING:*\n"
        "• Buka zona baru di *Shop → Buka Zona*\n"
        "• Zona berbeda = ore lebih berharga!\n"
        "• Mulai dari Permukaan → Void Realm\n\n"

        "🎁 *INVENTARIS & ITEM:*\n"
        "• Beli item consumable di *Shop → Item*\n"
        "• Gunakan item di *🎁 Inventaris*\n"
        "• ⚡ Energy Potion, 🍀 Luck Elixir, 💰 Double Coin, dll\n\n"

        "⭐ *LEVEL & XP:*\n"
        "• Mining menghasilkan XP\n"
        "• Level naik → unlock alat baru\n"
        "• Setiap level menambah daily bonus\n\n"

        "🎁 *DAILY BONUS:*\n"
        "• Klaim tiap 24 jam via *🎁 Daily*\n"
        "• Streak berturut = multiplier bonus!\n"
        "• Energy langsung penuh saat klaim\n\n"

        "🔥 *TIPS & TRIK:*\n"
        "• Upgrade alat sesegera mungkin\n"
        "• Gunakan Luck Elixir saat mining rare ore\n"
        "• Gabung streak harian untuk bonus besar\n"
        "• Buka zona baru untuk koin lebih besar\n"
        "• Rebirth Token: reset level tapi dapat bonus permanen!\n\n"

        "🔗 *REFERRAL:*\n"
        "Bagikan link di *👤 Profil*\n"
        "Kamu & temanmu dapat *300 koin* bonus!\n\n"

        "🏆 *PRESTASI:*\n"
        "Ada 12 prestasi dengan hadiah koin!\n"
        "Cek di *👤 Profil → Prestasi*"
    )
    await message.answer(text, reply_markup=back_main_kb(), parse_mode="Markdown")
