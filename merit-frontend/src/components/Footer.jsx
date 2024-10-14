const FooterTest = () => {

  return (
    <footer className="bg-gray-800 text-gray-400 py-8">
        <div className="max-container container grid  grid-cols-3 max-xl:grid-cols-2 max-sm:grid-cols-1 gap-8 p-7 ">
            <div>
                <h3 className="text-3xl text-white font-bold">MERIT</h3>
                <p className="max-w-md  leading-8 mt-2">Admission process made seamless with Merit. Helping students make the right choices when it comes to matters pertaining to course and institution.</p>
            </div>
            <div className="max-w-md">
                <h3 className="text-2xl text-white font-semibold">Quick Links</h3>
                <ul className="flex flex-col gap-4 mt-2">
                    <li className="hover:text-white">
                        <a href="/">Home</a>
                    </li>
                    <li className="hover:text-white">
                        <a href="/about">About us</a>
                    </li>
                    <li className="hover:text-white">
                        <a href="#">Services</a>
                    </li>
                    <li className="hover:text-white">
                        <a href="/service/aggregate-calculator">Aggrgrate Calculator</a>
                    </li>
                    <li className="hover:text-white">
                        <a href="/universities-list">Find Dream School</a>
                    </li>
                </ul>
            </div>
            <div className="flex flex-col gap-2  max-xl:col-span-2 max-sm:col-span-1">
                <p className="text-xl text-white font-semibold">Subscribe to our NewsLetter</p>
                <div className="flex items-center gap-3 w-full">
                    <input type="text" className=" p-2 rounded-md sm:mr-2  sm:mb-0 outline-none focus:ring-2 focus:ring-purple-500 max-xl:w-56"/>
                    <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md">Subscribe</button>
                </div>
            </div>
            <div className="text-center mt-8 text-gray-400 col-span-3 max-xl:cols-span-2 max-sm:col-span-1">
                &copy; {new Date().getFullYear()} Merit. All rights reserved.
            </div>
        </div>

    </footer>
  )
}

export default FooterTest