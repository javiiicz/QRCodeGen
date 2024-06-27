function Footer() {
    return (
        <footer className="static bg-[url('/src/images/Footer-background-2.png')] bg-cover bg-bottom">
            <div/>
                <div className="backdrop-blur-2xl border-t border-gray-200 flex flex-row-reverse justify-between h-40 md:px-72 sm:px-32 px-10">
                    <div className="text-4xl font-extrabold grid grid-rows-2 gap-0 items-center justify-items-center">
                        <p className="drop-shadow-lg">Socials</p>
                        <div className="grid grid-cols-2 gap-3">
                            <a
                            href="https://www.github.com/javiiicz"
                            className="w-12 h-12 bg-[url('/src/images/GitHub-Logo.svg')] bg-cover"
                            > </a>
                            <a
                            href="https://www.linkedin.com/in/jcarrilloz/"
                            className="w-12 h-12 bg-[url('/src/images/LinkedIn-Logo.svg')] bg-cover"
                            > </a>
                    </div>
                </div>
                <div className="grid grid-cols-1 gap-5 items-center justify-items-center">
                    <p>© 2024 Javier Carrillo</p>
                </div>
            </div>
        </footer>

    )
}

export default Footer;