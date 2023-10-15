'use client'

import { useEffect, useState } from "react";
import 'swiper/css';
import axios from 'axios';

enum Status {
  START,
  COURSESELECT,
  PROMPTING
}

export default function Home() {

  const [courseId, setCourseId] = useState(-1);
  const [status, setStatus] = useState(Status.START);
  const [courseButtonEnabled, setCourseButtonEnabled] = useState(false);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const getAnswer = async () => {
    const headers = {
      'Content-Type': 'application/json'
    };

    const body = {
      course_ids: [courseId.toString()],
      question: question
    };

    console.log(body)

    axios.post('http://localhost:2500/answer',
    body,
    {headers},
    ).then((response) => {
      setAnswer(response.data.answer);
  })
  }

  const detectCourseId = (courseLink : string) => {
    const courseNumber = courseLink.split('/');
    console.log(courseNumber);
    if (courseNumber.length < 5 || courseNumber[4] === '') {
      setCourseId(-1);
    } else {
      var id = parseInt(courseNumber[4]);
      setCourseId(id);
      if (Math.log10(id) > 5) {
        setCourseButtonEnabled(true);
      }
    }
  }


  const boxContents = () => {
    switch(status) {
      case Status.START:
        return(
          <>
            <h1 className='text-[52px] font-bold italic'>
              Hi I'm Tai!
              </h1>
            <p className='text-[24px] font-medium'>
                Your own personalized Teaching Assistant AI
            </p>
          
          <div className="w-full flex justify-end">
            <span className="button" onClick={() => setStatus(Status.COURSESELECT)}>Start</span>
            </div>
          </>
        )
      case Status.COURSESELECT:
        return(
          <>
            <h1 className='text-[52px] font-bold italic'>
              Course Selection
              </h1>
            <p className='text-[24px] font-medium'>
                Please select the course you want to use Tai for
            </p>
            <input className='canvasInput w-full p-4 my-5' 
            placeholder='Copy the link to your Canvas Course here'
            type='url'
            onChange={(e) => detectCourseId(e.target.value)}
            />
          <div className="w-full flex justify-between">
            <span className="button" onClick={() => setStatus(Status.START)}>Back</span>
            <span className={"button " + (!courseButtonEnabled && "disabled")} onClick={() => courseButtonEnabled && setStatus(Status.PROMPTING)}>Next</span>
            </div>
          </>
        )
        case Status.PROMPTING:
          return(
            <>
            <h1 className='text-[52px] font-bold italic'>
              Ask Away
              </h1>
            <p className='text-[24px] font-medium'>
                Now you can ask Tai any questions you have about the course!
            </p>
            <input className='canvasInput w-full p-4 my-5' 
            placeholder='Questions go here :D'
            type='text'
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            />
              {answer !== '' && 
            <div className="glass !w-full mb-3">
              <p className='text-[16px] font-medium'> 
                {answer}
              </p>
              <p className="text-[14px] font-thin">
                references go here
              </p>
            </div>
            }
            <div className="w-full flex justify-end">
              <span className="button" onClick={() => getAnswer()}>Ask</span>
            </div>
          </>
        )
    }
  }

  return (
    <main className="flex flex-col min-h-screen font-mono m-4 justify-center items-center">
          <div className="glass min-w-[55vw]">
              {boxContents()}
          </div>
    </main>
  )
}