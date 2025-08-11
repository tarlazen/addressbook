#!/usr/bin/env python3

import json
import os
import re
from typing import List, Dict, Optional

DATA_FILE = "address_book.json"

def load_data() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(entries: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def generate_id(entries: List[Dict]) -> int:
    if not entries:
        return 1
    return max(e["id"] for e in entries) + 1

def validate_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def validate_phone(phone: str) -> bool:
    return bool(re.match(r"^\+?[\d\s\-()]{6,}$", phone))

def add_contact(entries: List[Dict]) -> None:
    print("\n== Yeni Kişi Ekle ==")
    name = input("İsim: ").strip()
    if not name:
        print("İsim boş bırakılamaz.")
        return
    phone = input("Telefon: ").strip()
    email = input("E-posta: ").strip()
    address = input("Adres: ").strip()

    if email and not validate_email(email):
        print("Uyarı: Geçersiz e-posta formatı, kaydedilmiyor e-posta.")
        email = ""

    if phone and not validate_phone(phone):
        print("Uyarı: Telefon formatı doğru olmayabilir, yine de kaydedilsin mi? (E/h)")
        if input().lower() != "e":
            phone = ""

    new = {
        "id": generate_id(entries),
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }
    entries.append(new)
    save_data(entries)
    print(f"Kişi eklendi (id: {new['id']}).")

def list_contacts(entries: List[Dict]) -> None:
    print("\n== Kişiler ==")
    if not entries:
        print("Kayıtlı kişi yok.")
        return
    for e in entries:
        print(f"[{e['id']}] {e['name']} — Tel: {e.get('phone','-')} — Eposta: {e.get('email','-')}")
    print(f"\nToplam: {len(entries)} kişi.")

def find_contacts(entries: List[Dict], term: str) -> List[Dict]:
    term_lower = term.lower()
    results = [e for e in entries if term_lower in e['name'].lower()
               or term_lower in e.get('phone','').lower()
               or term_lower in e.get('email','').lower()
               or term_lower in e.get('address','').lower()]
    return results


def search_contacts(entries: List[Dict]) -> None:
    term = input("Arama terimi (isim/telefon/eposta/adres): ").strip()
    if not term:
        print("Arama terimi boş olamaz.")
        return
    results = find_contacts(entries, term)
    if not results:
        print("Eşleşen kayıt bulunamadı.")
        return
    print(f"\n{len(results)} sonuç:")
    for e in results:
        print(json.dumps(e, ensure_ascii=False, indent=2))

def get_contact_by_id(entries: List[Dict], cid: int) -> Optional[Dict]:
    for e in entries:
        if e["id"] == cid:
            return e
    return None

def update_contact(entries: List[Dict]) -> None:
    try:
        cid = int(input("Güncellenecek kişinin ID'si: "))
    except ValueError:
        print("Geçersiz ID.")
        return
    person = get_contact_by_id(entries, cid)
    if not person:
        print("Kişi bulunamadı! Lütfen kontrol edin.")
        return
    print("Boş bırakırsanız mevcut değer korunur.")
    name = input(f"İsim ({person['name']}): ").strip() or person['name']
    phone = input(f"Telefon ({person.get('phone','')}): ").strip() or person.get('phone','')
    email = input(f"E-posta ({person.get('email','')}): ").strip() or person.get('email','')
    address = input(f"Adres ({person.get('address','')}): ").strip() or person.get('address','')

    if email and not validate_email(email):
        print("Uyarı: e-posta geçersiz, e-posta alanı temizlenmiştir.")
        email = ""

    person.update({"name": name, "phone": phone, "email": email, "address": address})
    save_data(entries)
    print("Güncelleme yapıldı.")

def delete_contact(entries: List[Dict]) -> None:
    try:
        cid = int(input("Silinecek kişinin id'si: "))
    except ValueError:
        print("Geçersiz id.")
        return
    person = get_contact_by_id(entries, cid)
    if not person:
        print("Kişi bulunamadı.")
        return
    confirm = input(f"{person['name']} silinsin mi? (E/h): ").lower()
    if confirm == "e":
        entries.remove(person)
        save_data(entries)
        print("Kişi silindi.")
    else:
        print("İşlem iptal edilmiştir.")

def pretty_print_full(entries: List[Dict]) -> None:
    for e in entries:
        print("-" * 40)
        print(f"id: {e['id']}")
        print(f"İsim: {e['name']}")
        print(f"Telefon: {e.get('phone','-')}")
        print(f"E-posta: {e.get('email','-')}")
        print(f"Adres: {e.get('address','-')}")
    print("-" * 40)

def main_loop():
    entries = load_data()
    menu = """
Adres Defteri
1) Kişi ekle
2) Kişileri listele (kısa)
3) Kişileri listele (detay)
4) Ara
5) Güncelle
6) Sil
7) Çıkış
Seçiminiz: """
    while True:
        choice = input(menu).strip()
        if choice == "1":
            add_contact(entries)
        elif choice == "2":
            list_contacts(entries)
        elif choice == "3":
            pretty_print_full(entries)
        elif choice == "4":
            search_contacts(entries)
        elif choice == "5":
            update_contact(entries)
        elif choice == "6":
            delete_contact(entries)
        elif choice == "7":
            print("Görüşürüz!")
            break
        else:
            print("Geçersiz seçim, tekrar deneyin!")


if __name__ == "__main__":
    main_loop()
