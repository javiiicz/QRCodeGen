function Header() {
    return (
        <header className="bg-gray-200/50 z-50 sticky top-0 backdrop-blur-md sm:p-0 p-4 shadow-sm">
            <nav className="grid sm:grid-cols-2 sm:grid-rows-1 gap-4 px-20 sm:h-16 h-8 grid-rows-1 grid-cols-1">
                <div className="h-full flex items-center px-5 justify-center sm:justify-start">
                    <a href="https://javiiicz.github.io" className="text-gray-900 text-xl font-extrabold italic drop-shadow-md hover:text-[1.28rem] transition-all duration-[800ms]">Javier Carrillo</a>
                </div>
            </nav>
        </header>
    );
}

export default Header;