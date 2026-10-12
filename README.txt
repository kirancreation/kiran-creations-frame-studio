KIRAN CREATIONS FRAME STUDIO PRO — UPDATED ZIP

CHANGES IN THIS VERSION
• Removed the separate Photo Settings panel to save space.
• Mouse drag remains for moving objects; use the corner handles to resize proportionally or freely.
• Removed the Canvas Size dropdown. Use A4 Preview / A3 Preview buttons and the JPG export choices.
• Added a phone-upload QR feature. Uploads from your phone appear in the Photo Gallery automatically.

HOW TO RUN THE APP
1. Extract the whole ZIP folder.
2. On Windows, double-click start_server.bat. Keep its black command window open.
3. Open http://127.0.0.1:8000 in Chrome on the computer.
4. Computer and phone must be on the same Wi-Fi network. Allow Python through Windows Firewall on a private network if asked.
5. The QR code in Photo Gallery opens the mobile upload page. Select photos and tap Upload; they should appear in the gallery within a few seconds.

NOTES
• Python 3 is required on the computer for mobile QR uploads. If Python is not installed, install Python 3 and run start_server.bat again.
• QR rendering uses an online QR image service, so internet is needed to display the QR image. The app/server and mobile upload work on the local Wi-Fi.
• Keep start_server.bat running during use. The QR mobile upload works only while the computer is running the server and both devices share the same Wi-Fi/LAN. Guest Wi-Fi/client isolation or firewall rules may block access.
• Images are saved in the included uploads folder and shown in the browser gallery.
• JPG export uses html2canvas from a CDN, so internet is required for export if that library has not loaded.
• This is a standalone local app ZIP and does not automatically change the GitHub repository.


QR CODE UPDATE
The QR code is generated locally by the bundled Python QR module and appears in the Photo Gallery panel when the app is opened through start_server.bat. No external QR-code website is needed. Keep the server window open, and keep the phone and computer on the same Wi-Fi. Scan the QR displayed inside the app to upload photos directly into the gallery.


NEW FEATURES:
- Print button: choose A4 or A3 Preview first, then click Print and select your printer or Save as PDF in the browser print dialog.
- WhatsApp button: opens a chat to Kiran Creations at +91 76796 43645.
Note: This ZIP is a standalone updated copy. To change the live GitHub Pages website, upload/commit the updated index.html (and keep the other existing project files) to the repository.
