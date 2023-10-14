import Image from 'next/image'

export default function Home() {
  return (
    <main className="flex flex-col min-h-screen font-mono m-4">
        <h1 className='text-[52px] font-bold italic'>
          Hi I'm Tai!
          </h1>
        <p className='text-[24px] font-medium'>
          Your own personalized Teaching Assistant AI
        </p>
     
     
     {/* Getting Started Section */}
     <div className='flex p-5 pl-0 items-center'>
        <h2>To start: Copy the link of your Canvas course here --> </h2>
        <input className='canvasInput ml-4 p-1' placeholder='Link goes here :3' />
     </div>
     
    </main>
  )
}
