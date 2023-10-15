"use client";

import { useState } from "react";
import "swiper/css";
import axios from "axios";
import { stat } from "fs";

enum Status {
  START,
  COURSESELECT,
  PROMPTING,
}

type Reference = {
  citation_no: number,
  course_id: string,
  file_name: string,
  link: string,
  name: string,
  page_number: string,
  source_window: string
}

type PromptAnswer = {
  question: string,
  response: {
    answer: string,
    citations: Reference[]
  }
}

export default function Home() {
  const [courseId, setCourseId] = useState(-1);
  const [status, setStatus] = useState(Status.START);
  const [courseButtonEnabled, setCourseButtonEnabled] = useState(false);
  const [question, setQuestion] = useState('');
  const [canAsk, setCanAsk] = useState(true);

  const [promptAnswers, setPromptAnswers] = useState<PromptAnswer[]>([]);


  const getAnswer = async () => {
    const headers = {
      "Content-Type": "application/json",
    };

    const body = {
      course_ids: [courseId.toString()],
      question: question,
    };

    setCanAsk(false);

    axios.post('/answer',
    body,
    {headers},
    ).then((response) => {
      const newEntry : PromptAnswer = {
        question: question,
        response: response.data
      }
      setPromptAnswers([newEntry, ...promptAnswers]);
      setCanAsk(true);
      setQuestion('');
  })
  
  }

  const detectCourseId = (courseLink: string) => {
    const courseNumber = courseLink.split("/");
    console.log(courseNumber);
    if (courseNumber.length < 5 || courseNumber[4] === "") {
      setCourseId(-1);
    } else {
      var id = parseInt(courseNumber[4]);
      setCourseId(id);
      if (Math.log10(id) > 4) {
        setCourseButtonEnabled(true);
      }
    }
  };

  const boxContents = () => {
    switch (status) {
      case Status.START:
        return (
          <>
            <h1 className="text-[52px] font-bold italic">Hi, I'm Tai!</h1>
            <p className="text-[24px] font-medium">
              Your own personalized Teaching Assistant AI
            </p>

            <div className="w-full flex justify-end">
              <span
                className="button"
                onClick={() => setStatus(Status.COURSESELECT)}
              >
                Start
              </span>
            </div>
          </>
        );
      case Status.COURSESELECT:
        return (
          <>
            <h1 className="text-[52px] font-bold italic">Course Selection</h1>
            <p className="text-[24px] font-medium">
              Please select the course you want to use Tai for
            </p>
            <input
              className="canvasInput w-full p-4 my-5"
              placeholder="Copy the link to your Canvas Course here"
              type="url"
              onChange={(e) => detectCourseId(e.target.value)}
            />
            <div className="w-full flex justify-between">
              <span className="button" onClick={() => setStatus(Status.START)}>
                Back
              </span>
              <span
                className={"button " + (!courseButtonEnabled && "disabled")}
                onClick={() =>
                  courseButtonEnabled && setStatus(Status.PROMPTING)
                }
              >
                Next
              </span>
            </div>
          </>
        );
      case Status.PROMPTING:
        return (
          <>
            <h1 className="text-[52px] font-bold italic">Ask Away</h1>
            <p className="text-[24px] font-medium">
              Now you can ask Tai any questions you have about the course!
            </p>
            <input
              className="canvasInput w-full p-4 my-5"
              placeholder="Questions go here :D"
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <div className="w-full flex justify-end mb-5">
              <span className={"button " + (!canAsk && "disabled")} onClick={() => canAsk && getAnswer()}>Ask</span>
            </div>
            {promptAnswers.map((answer) => {
              return(
                <div className="glass !w-full mb-3">
                  <p className='text-[16px] font-bold mb-2'> 
                    {answer?.question}
                  </p>
                  <p className='text-[16px] font-medium mb-2'> 
                    {answer?.response.answer}
                  </p>
                  <p className="text-[14px] font-thin">
                    {
                      answer?.response.citations.map((ref) => {
                        return(
                          <p className="text-[14px] font-thin">
                            {'[' + ref.citation_no + '] '} {
                           ref.link ? 
                            <a className="underline link" href={ref.link}>
                              {ref.name}
                            </a> : ref.name
                            } {ref.page_number && ("| Page " + ref.page_number)}
                          </p>
                        )
                      })
                    }
                  </p>
                </div>
              )
            })
          }
        <span className="text-center !justify-self-end font-light">While these results are a good first step, the information returned by the language model may not be completely accurate. Make sure to read the source material yourself.</span>
          </>
        );
      }
  };

  return (
    <main className="flex flex-col min-h-screen font-mono m-4 justify-center items-center">
      <div className="glass min-w-[55vw]">{boxContents()}</div>
      {status === Status.COURSESELECT && (
        <div className="glass min-w-[55vw] mt-5">
          <p className="text-[17px] font-medium flex flex-col">
            For demo purposes, you can use one of these courses:
          </p>
          <p className="font-thin my-3">
            Computer Networks: https://gatech.instructure.com/courses/324194
          </p>
          <p className="font-thin my-3">
            Intro Cyber Phys Sys Sec: https://gatech.instructure.com/courses/352034
          </p>
          <p className="font-thin my-3">
            Mobile & Ubiquitous Comp: https://gatech.instructure.com/courses/334454
          </p>
          <p className="font-thin my-3">
            Comp. Org & Program: https://gatech.instructure.com/courses/118080
          </p>
          <p className="font-thin my-3">
            Data Structures and Algoirthms: https://gatech.instructure.com/courses/91004
          </p>
          <p className="font-thin my-3">
            Objects & Design: https://gatech.instructure.com/courses/137180
          </p>
        </div>
      )}

    </main>
  );
}
