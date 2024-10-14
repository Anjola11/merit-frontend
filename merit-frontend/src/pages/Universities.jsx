import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import Aggregator from "./Services/Aggregator";
import arrowRight from "../assets/arrow-right.png"

const Universities = () => {
  const [universities, setUniversities] = useState([]);
  const [course, setCourse] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();

  const BASE_URL = "http://127.0.0.1:5000"; // Your API base URL

  useEffect(() => {
    const courseName = searchParams.get("course_name");
    if (courseName) {
      fetchUniversities(courseName);
    }
  }, [searchParams]);

  const fetchUniversities = async (courseName) => {
    try {
      const response = await fetch(
        `${BASE_URL}/universities/courses?course_name=${encodeURIComponent(
          courseName
        )}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch universities");
      }
      const result = await response.json();

      setUniversities(result["Universities offering the course"]); // Extracting the universities array
      setCourse(result.course); // Set the course name if needed
    } catch (error) {
      console.error("Error fetching universities:", error);
      setError("Failed to load universities");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {!loading && universities.length > 0 && (
        <div>
          <h2 className="text-3xl">Universities offering <span className="font-bold">{course}</span></h2>
          <table>
            <thead>
              <tr>
                <th className="text-xl">Universities</th>
              </tr>
            </thead>
            <tbody>
              {universities.map((university, index) => (
                <tr key={index}>
                  <td>{university}</td>
                </tr>
              ))}
            </tbody>
          </table>

        </div>
      )}
      {!loading && universities.length === 0 && (
        <p>No universities found for the selected course.</p>
      )}
      {/* <a
        href={`uni?university_name=${encodeURIComponent(
          "University of Lagos (UNILAG)"
        )}`}
      >
        Obafemi Awolowo University (OAU)
      </a> */}
      <div>
        <h2 className="mt-9 mb-3 font-semibold">
          USE OUR AGGREGATOR APP TO SEE YOUR CHANCES OF ADMISSION
        </h2>
        <a href="/service/aggregate-calculator" >
          <div className="bg-[#5c48ee] flex justify-center items-center gap-2 w-max py-2 px-4 rounded-full text-white">
            <p>Check Now</p>
            <div className=" bg-white rounded-full"><img src={arrowRight} width={25} height={25} alt="" /></div>
          </div>
        </a>
      </div>
    </div>
  );
};

export default Universities;
