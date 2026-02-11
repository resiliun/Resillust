import * as React from 'react';

// INI KUNCI PERBAIKANNYA: 
// Daftarin variabel baru lu di sini biar TypeScript nggak marah lagi
interface ContactUsEmailProps {
  senderName: string;
  senderEmail: string;
  category: string;      // Tambahkan ini
  packageName: string;   // Tambahkan ini
  description: string;   // Tambahkan ini
}

export const Commission = ({
  senderName,
  senderEmail,
  category,
  packageName,
  description,
}: ContactUsEmailProps) => (
  <div style={{ fontFamily: 'sans-serif', padding: '20px', color: '#333' }}>
    <h2>Commission Request Baru 🎨</h2>
    <p><strong>Dari:</strong> {senderName} ({senderEmail})</p>
    <hr />
    <p><strong>Type:</strong> {category}</p>
    <p><strong>Coverage:</strong> {packageName}</p>
    <p><strong>Deskripsi:</strong></p>
    <div style={{ padding: '10px', background: '#f4f4f4', borderRadius: '5px' }}>
      {description}
    </div>
  </div>
);