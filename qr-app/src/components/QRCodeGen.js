import React, { useState } from 'react';
import {Message} from '../scripts/QRGen.js'

function QRCodeGen() {
    const [text, setText] = useState('') // Text state
    const [radio, setRadio] = useState('L') // Radio State defaul "L"
    const [qrCodeImage, setQRCodeImage] = useState(null)
    
    const generateQRCode =  () => {
        try {
            const m = new Message(text, radio)
            const encoded_image = m.createImage();
            setQRCodeImage(encoded_image);
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
                <button onClick={generateQRCode}>Generate !</button>
                { qrCodeImage && (
                    <img className="w-[60%] mx-auto my-10" src={qrCodeImage} alt="Generated QR Code"/>
                )}
            </div>
        </div>
    );
}

export default QRCodeGen;