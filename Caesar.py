import flet as ft
import random
import os
import tempfile

# Caesar cipher and ROT13 functions remain the same
def caesar_encrypt(plain_text, shift, char_set="alphabet"):
    result = ""
    for char in plain_text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        elif char_set == "extended" and char.isdigit():
            result += chr((ord(char) - 48 + shift) % 10 + 48)
        else:
            result += char
    return result

def caesar_decrypt(cipher_text, shift, char_set="alphabet"):
    result = ""
    for char in cipher_text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        elif char_set == "extended" and char.isdigit():
            result += chr((ord(char) - 48 - shift) % 10 + 48)
        else:
            result += char
    return result

def rot13(text):
    result = []
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result.append(chr((ord(char) - shift_base + 13) % 26 + shift_base))
        else:
            result.append(char)
    return "".join(result)

def main(page: ft.Page):
    page.title = "Caesar Cipher Encryption/Decryption"
    page.padding = 20
    page.window_width = 600
    page.window_height = 800

    # File picker setup remains the same
    def handle_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            try:
                file_path = e.files[0].path
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    message_input.value = content
                    page.update()
            except Exception as ex:
                page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error reading file: {str(ex)}")))
                page.update()

    # Create file picker and save file dialog
    file_picker = ft.FilePicker(on_result=handle_file_result)
    save_file_dialog = ft.FilePicker(
        on_result=lambda e: handle_save_file(e) if e.path else None
    )
    
    page.overlay.extend([file_picker, save_file_dialog])

    def handle_save_file(e):
        try:
            with open(e.path, 'w', encoding='utf-8') as file:
                file.write(encrypted_output.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"File saved successfully to: {e.path}")))
        except Exception as ex:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error saving file: {str(ex)}")))
        page.update()

    # Widgets remain the same
    message_input = ft.TextField(
        label="Enter Message",
        multiline=True,
        min_lines=3,
        max_lines=5,
        expand=True
    )
    
    shift_input = ft.TextField(
        label="Enter Shift Value",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )
    
    encrypted_output = ft.Text(
        selectable=True,
        style=ft.TextStyle(size=16),
        text_align=ft.TextAlign.LEFT,
        width=float('inf')
    )
    
    decrypted_output = ft.Text(
        selectable=True,
        style=ft.TextStyle(size=16),
        text_align=ft.TextAlign.LEFT,
        width=float('inf')
    )

    char_set_selector = ft.Dropdown(
        label="Character Set",
        options=[
            ft.dropdown.Option("Alphabet Only"),
            ft.dropdown.Option("Letters + Digits + Special Characters")
        ],
        value="Alphabet Only",
        width=300
    )

    # Actions
    def encrypt_action(e):
        message = message_input.value.strip()
        char_set = "alphabet" if char_set_selector.value == "Alphabet Only" else "extended"
        try:
            shift = int(shift_input.value) if shift_input.value else generate_random_shift()
            if not message:
                encrypted_output.value = "Message cannot be empty."
            else:
                encrypted_text = caesar_encrypt(message, shift, char_set)
                encrypted_output.value = f"Encrypted (Shift {shift}): {encrypted_text}"
            page.update()
        except ValueError:
            encrypted_output.value = "Invalid shift value. Please enter an integer."
            page.update()

    def decrypt_action(e):
        encrypted_text = encrypted_output.value
        if not encrypted_text:
            decrypted_output.value = "No encrypted text to decrypt."
            page.update()
            return

        # Handle ROT13
        if encrypted_text.startswith("ROT13 Encrypted:"):
            try:
                encrypted_text = encrypted_text.split(": ", 1)[1]
                decrypted_text = rot13(encrypted_text)  # ROT13 is its own inverse
                decrypted_output.value = f"Decrypted (ROT13): {decrypted_text}"
                page.update()
                return
            except IndexError:
                encrypted_text = ""

        # Handle Caesar cipher
        if encrypted_text.startswith("Encrypted (Shift"):
            try:
                encrypted_text = encrypted_text.split(": ", 1)[1]
            except IndexError:
                encrypted_text = ""

        char_set = "alphabet" if char_set_selector.value == "Alphabet Only" else "extended"
        try:
            shift = int(shift_input.value) if shift_input.value else generate_random_shift()
            if not encrypted_text:
                decrypted_output.value = "No encrypted text to decrypt."
            else:
                decrypted_text = caesar_decrypt(encrypted_text, shift, char_set)
                decrypted_output.value = f"Decrypted (Shift {shift}): {decrypted_text}"
            page.update()
        except ValueError:
            decrypted_output.value = "Invalid shift value. Please enter an integer."
            page.update()

    def generate_random_shift():
        return random.randint(1, 25)

    def rot13_action(e):
        message = message_input.value.strip()
        if not message:
            encrypted_output.value = "Message cannot be empty."
        else:
            encrypted_text = rot13(message)
            encrypted_output.value = f"ROT13 Encrypted: {encrypted_text}"
        page.update()

    def clear_action(e):
        message_input.value = ""
        shift_input.value = ""
        encrypted_output.value = ""
        decrypted_output.value = ""
        page.update()

    def export_action(e):
        if not encrypted_output.value:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("No encrypted message to export!")))
            return
        save_file_dialog.save_file(
            file_name="encrypted_message.txt",
            allowed_extensions=["txt"]
        )
        page.update()

    # Buttons
    buttons_row1 = ft.Row(
        controls=[
            ft.ElevatedButton("Encrypt", on_click=encrypt_action),
            ft.ElevatedButton("Decrypt", on_click=decrypt_action),
            ft.ElevatedButton("Apply ROT13", on_click=rot13_action)
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    buttons_row2 = ft.Row(
        controls=[
            ft.ElevatedButton("Clear", on_click=clear_action),
            ft.ElevatedButton(
                "Upload File",
                on_click=lambda _: file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["txt"]
                )
            ),
            ft.ElevatedButton("Export", on_click=export_action)
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Layout
    page.add(
        ft.Column(
            controls=[
                message_input,
                ft.Row([shift_input, char_set_selector]),
                buttons_row1,
                ft.Container(content=encrypted_output, padding=10),
                ft.Container(content=decrypted_output, padding=10),
                buttons_row2
            ],
            spacing=20
        )
    )

ft.app(target=main)