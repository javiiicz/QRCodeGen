import React, { useState } from 'react';
import axios from 'axios';

function QRCodeGen() {
    const [text, setText] = useState('') // Text state
    const [radio, setRadio] = useState('L') // Radio State defaul "L"
    const [qrCodeImage, setQRCodeImage] = useState(null)
    
    const generateQRCode = async () => {
        const data = {text: text, radio: radio}
        try {
            const response = await axios.post('/generate_qr', data, {headers: {"Content-Type": "application/json"}}); // Send data to backend
            const encoded_image = response.data.image;
            setQRCodeImage(`data:image/png;base64,${encoded_image}`); // Create image URL
        } catch (error) {
            console.error('Error generating QR code:', error);
        }
    };
    
    const handleText = (event) => {
        setText(event.target.value);
    }
    
    const handleRadio = (event) => {
        setRadio(event.target.value);
    }
    
    return (
        <div className = "px-[10%] py-10">
            <h1 className="font-black text-4xl">QR Code Generator</h1>
            <p>Short description</p>
            <div >
                <form className="text-center grid grod-rows-3" onSubmit={(e) => {
                          e.preventDefault()
                          generateQRCode()
                      }}>
                    <input type="text" value={text} onChange={handleText}></input>
                    <div className="flex flex-row gap-3 align-center">
                        <label>
                            <input type="radio" value="L" checked={radio === 'L'} onChange={handleRadio} />
                            L
                        </label>
                        <label>
                            <input type="radio" value="M" checked={radio === 'M'} onChange={handleRadio} />
                            M
                        </label>
                        <label>
                            <input type="radio" value="Q" checked={radio === 'Q'} onChange={handleRadio} />
                            Q
                        </label>
                        <label>
                            <input type="radio" value="H" checked={radio === 'H'} onChange={handleRadio} />
                            H
                        </label>
                    </div>
                    <button type="submit">Generate !</button>
                </form>    
                { qrCodeImage && (
                    <img className="w-[60%] mx-auto my-10" src={qrCodeImage} alt="Generated QR Code"/>
                )}
            </div>
        </div>
    );
}

export default QRCodeGen;