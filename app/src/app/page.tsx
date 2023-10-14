'use client'

import { useEffect, useState } from "react";

export default function Home() {

  const [courseId, setCourseId] = useState(-1);
  const [response, setResponse] = useState('')

  useEffect(() => {
    if (courseId !== -1) {
      const socket =  new WebSocket("ws://127.0.0.1:5000/ask");
  
      socket.onopen = (event) => {
        console.log("WebSocket connection opened:", event);
        socket.send(courseId.toString());
    };
    
    socket.onmessage = (event) => {
        console.log("Received message:", event.data);
        setResponse(event.data);
    };
    
    socket.onclose = (event) => {
        console.log("WebSocket connection closed:", event);
    };
  
      }
  }, [courseId])


  const detectCourseId = (courseLink : string) => {
    const courseNumber = courseLink.split('/');
    console.log(courseNumber);
    if (courseNumber.length < 5 || courseNumber[4] === '') {
      setCourseId(-1);
    } else {
      setCourseId(parseInt(courseNumber[4]))
    }
  }


  return (
    <main className="flex flex-col min-h-screen font-mono m-4">
        <h1 className='text-[52px] font-bold italic'>
          Hi I'm Tai!
          </h1>
        <p className='text-[24px] font-medium'>
          Your own personalized Teaching Assistant AI
        </p>
     
     
     {/* Getting Started Section */}
     <div className='mt-5'>
      <h2>Getting Started :p</h2>
      <div className="mt-2">
      <span>1.</span>
        <input className='canvasInput p-1' 
               placeholder='Copy the link to your Canvas Course here'
               type='url'
              onChange={(e) => detectCourseId(e.target.value)}
               />
      </div>
      <div className="mt-2">
        <span>2.</span>
        <button>{response}</button>
      </div>
     </div>
     
    </main>
  )
}
