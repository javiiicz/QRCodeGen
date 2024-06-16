import React, {useState} from 'react';
import {Message} from '../scripts/QRGen.js'

function QRCodeGen() {
    const [text, setText] = useState('') // Text state
    const [radio, setRadio] = useState('L') // Radio State defaul "L"
    const [qrCodeImage, setQRCodeImage] = useState(null)

    const generateQRCode = () => {
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
        <div className="relative px-[10%] py-10">
            <h1 className="font-black text-4xl pb-5 relative z-10">QR Code Generator</h1>

            <p className="font-semibold">This QR Code generator was originally coded in Python and then ported to
                JavaScript. It was made
                following <a href="https://www.thonky.com/qr-code-tutorial/introduction"
                             className="font-bold underline text-blue-500">this tutorial</a>.
            </p>

            <svg className="absolute w-[450px] right-[40px] -bottom-[50px]" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                <path fill="#FA4D56"
                    d="M58,-42.2C72.5,-28.2,79.6,-4.2,74.1,15.7C68.6,35.6,50.5,51.5,32.4,55.9C14.2,60.3,-4,53.2,-19.6,44.3C-35.2,35.4,-48.1,24.7,-52.1,10.9C-56,-2.9,-51,-19.8,-40.8,-32.8C-30.6,-45.8,-15.3,-54.9,3.2,-57.5C21.8,-60.1,43.6,-56.1,58,-42.2Z"
                    transform="translate(100 100)"/>
            </svg>

            <svg className="absolute w-[380px] left-[15px] top-[130px]" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                <path fill="#F1C21B" d="M39.2,-23.2C53.6,-13.1,70.2,3.3,66.4,13.1C62.5,22.9,38.3,26.1,21.1,28.5C3.9,30.8,-6.2,32.4,-16,29.3C-25.9,26.1,-35.3,18.2,-37.8,8.3C-40.3,-1.5,-35.7,-13.2,-28.3,-21.6C-20.8,-30.1,-10.4,-35.2,1,-36C12.4,-36.8,24.7,-33.2,39.2,-23.2Z" transform="translate(100 100)" />
                </svg>


            <div className="m-4 backdrop-blur bg-gray-100/50 md:px-10 px-8 py-2 shadow-glass rounded-xl">

                <p className="font-medium py-2">Write the message to be encoded in the text box and select the error
                    correction level. Then, click the generate button to obtain your
                    QR code.</p>

                <div className="grid lg:grid-cols-2 lg:grid-rows-1 grid-rows-2 grid-cols-1 py-4 items-center">
                    <div className="flex flex-col items-center gap-10">
                        <div className="md:w-[80%] w-full">
                            <p className="font-bold">Text String:</p>
                            <textarea
                                className="border-[1px] border-gray-200 rounded h-36 w-full pb-28 max-h-52 px-1 text-gray-700"
                                placeholder="Enter text to be put into QR Code" value={text}
                                onChange={handleText}></textarea>
                        </div>

                        <div>
                            <p className="font-bold">Error Correction Level:</p>
                            <div className="flex flex-row flex-wrap gap-5 align-center">
                                <div>
                                    <input type="radio" value="L" checked={radio === 'L'} onChange={handleRadio}/>
                                    <label> Low </label>
                                </div>

                                <div>
                                    <input type="radio" value="M" checked={radio === 'M'} onChange={handleRadio}/>
                                    <label> Medium </label>
                                </div>

                                <div>
                                    <input type="radio" value="Q" checked={radio === 'Q'} onChange={handleRadio}/>
                                    <label> Quartile</label>
                                </div>

                                <div>
                                    <input type="radio" value="H" checked={radio === 'H'} onChange={handleRadio}/>
                                    <label> High</label>
                                </div>


                            </div>
                        </div>
                        <button className="font-extrabold bg-red-500 text-white p-3 rounded-xl"
                                onClick={generateQRCode}>Generate !
                        </button>
                    </div>


                    <div className="max-w-96 max-h-96 mx-auto my-10">
                        {!qrCodeImage && (
                            <div className="w-full h-full bg-gray-300 rounded-xl"/>
                        )}

                        {qrCodeImage && (
                            <img className="w-full h-full rounded-xl" src={qrCodeImage} alt="Generated QR Code"/>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default QRCodeGen;