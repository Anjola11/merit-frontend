import { useState, useEffect } from 'react';
import './Aggregator.css';

const BASE_URL = 'http://127.0.0.1:5000';

function Aggregator() {
  const [universities, setUniversities] = useState([]); // List of universities
  const [university, setUniversity] = useState(''); // Selected university
  const [courses, setCourses] = useState([]); // List of courses based on selected university
  const [selectedCourse, setSelectedCourse] = useState(''); // Selected course
  const [utme_score, setUtme_score] = useState(); // UTME score
  const [utmeError, setUtmeError] = useState(''); // State for UTME score error message
  const [postUtme_score, setPostUtme_score] = useState(); // Post UTME score
  const [postUtmeError, setPostUtmeError] = useState(''); // State for Post UTME score error message
  const [maxPostUtmeScore, setMaxPostUtmeScore] = useState(100); // Maximum Post UTME score
  const [olevel, setOlevel] = useState(''); // Olevel grades
  const [data, setData] = useState(null); // Fetched data
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(''); // Error state
  const [olevel_required, setOlevel_required] = useState(false) // State for Olevel required
  const [postUtme_required, setPostUtme_required] = useState(false) // State for Post Utme required
  const [sitting_required, setSitting_required] = useState(false)
  const [sitting, setSitting] = useState('')
  const [missingInfo, setMissingInfo] = useState([])
  const [missingInfoError, setMissingInfoError] = useState("")
  const [isButtonClicked, setisButtonClicked] = useState(false)
 
  // Fetch the university list when the component mounts
  useEffect(() => {
    const fetchUniversities = async () => {

      setLoading(true);
      try {
        const response = await fetch(`${BASE_URL}/universities/list`);
        if (!response.ok) {
          throw new Error('Failed to fetch universities');
        }
        const result = await response.json();
        const universitiesList = result['Supported Universities'] || [];
        setUniversities(universitiesList); // Set the universities in state
      } catch (error) {
        console.error('Error fetching universities:', error);
        setError('Failed to load universities');
      } finally {
        setLoading(false);
      }
    };

    fetchUniversities();
  }, []); // Run on mount

  // Fetch max Post UTME score when a university is selected
  const fetchPostUtmeRequirements = async (selectedUniversity) => {
    setData('')
    setOlevel_required(false);
    setPostUtme_required(false);
    setSitting_required(false)
    setSitting('')
    setUtme_score('')
    setPostUtme_score('')
    setError('')
    try {
      const response = await fetch(
        `${BASE_URL}/universities/aggregate-requirements?university_name=${selectedUniversity}`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch Post UTME requirements');
      }
      const result = await response.json();
      setMaxPostUtmeScore(result[`aggregate requirements`].max_post_utme); // Set the maximum Post UTME score
      if(result[`aggregate requirements`].method === 'utme_postutme_olevel'){
        setPostUtme_required(true)
        setOlevel_required(true)
      }
      else if(result[`aggregate requirements`].method === 'utme_olevel'){
        setOlevel_required(true)
      }
      else if(result[`aggregate requirements`].method === 'utme_postutme'){
        setPostUtme_required(true)
      }
      if(result[`aggregate requirements`].sitting){
        setSitting_required(true)
      }

    } catch (error) {
      console.error('Error fetching Post UTME requirements:', error);
    }
  };

  // Fetch courses when a university is selected
  const fetchCourses = async (selectedUniversity) => {
    if (!selectedUniversity) {
      console.error('No university selected!');
      setCourses([]); // Reset courses if no university is selected
      return; // Exit the function early if no university is selected
    }

    setLoading(true);
    setCourses([]); // Reset courses when fetching new ones
    try {
      const url = `${BASE_URL}/universities/list/courses?university_name=${encodeURIComponent(
        selectedUniversity
      )}`;
      const response = await fetch(url);

      if (!response.ok) {
        const errorMessage = await response.text(); // Get the error response body
        throw new Error(
          `HTTP error! status: ${response.status}, message: ${errorMessage}`
        );
      }

      const result = await response.json();
      setCourses(result['List of courses'] || []); // Correct key to access courses
    } catch (error) {
      console.error('Error fetching courses:', error);
      setError('Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  // Update university and fetch courses
  const updateUniversity = (event) => {
    const selectedUniversity = event.target.value;
    setUniversity(selectedUniversity); // Set the selected university
    fetchCourses(selectedUniversity); // Fetch courses for the selected university
    fetchPostUtmeRequirements(selectedUniversity)
    
  };

  // Update selected course
  const updateCourse = (event) => {
    setSelectedCourse(event.target.value); // Update the selected course
  };

  // Update UTME score
  const updateUtme_score = (event) => {
    setMissingInfoError('')
    const value = event.target.value;

    // Allow empty input for clearing the field
    if (value === '') {
      setUtme_score(''); // Set to empty string to clear
      setUtmeError(''); // Clear error message when input is empty
      return;
    }

    // Convert value to a number
    const numberValue = Number(value);

    // Update state only if the value is valid
    if (numberValue >= 0 && numberValue <= 400) {
      setUtme_score(numberValue);
      setUtmeError(''); // Clear error message if valid
    } else {
      setUtmeError('Score should be <= 400'); // Set error message if invalid
    }
  };

  // Handle blur event to validate the score
  const handleBlur = () => {
    const numberValue = Number(utme_score); // Convert the current score to a number
    if (numberValue < 0 || numberValue > 400) {
      setUtmeError('Score should be <= 400');
    }
  };

  // Update Post UTME score
  const updatePostUtme_score = (event) => {
    setMissingInfoError('')
    const value = event.target.value;

    // Allow empty input for clearing the field
    if (value === '') {
      setPostUtme_score('');
      setPostUtmeError(''); // Clear error message when input is empty
      return;
    }

    // Convert value to a number
    const numberValue = Number(value);

    // Update state only if the value is valid
    if (numberValue >= 0 && numberValue <= maxPostUtmeScore) {
      setPostUtme_score(numberValue);
      setPostUtmeError(''); // Clear error message if valid
    } else {
      setPostUtmeError(`Score should be <= ${maxPostUtmeScore}`); // Set error message if invalid
    }
  };

  // Handle blur event to validate the score
  const handlePostUtmeBlur = () => {
    if (postUtme_score < 0 || postUtme_score > maxPostUtmeScore) {
      setPostUtmeError(`Score should be <= ${maxPostUtmeScore}`);
    }
  };

  // Update Olevel grades

  const [formData, setFormData] = useState({
    olevelResults: {
      mathematics: '',
      english: '',
      subject1: '',
      subject2: '',
      subject3: '',
    },
  });

  const grades = ['A1', 'B2', 'B3', 'C4', 'C5', 'C6', 'D7', 'F9'];

  const handleChange = (event) => {
    setMissingInfoError('')
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      olevelResults: {
        ...prevData.olevelResults,
        [name]: value,
      },
    }));
    
  };
  const updateSitting = (event) => {
    setMissingInfoError('')
    const value = event.target.value;
    const sittingValue = Number(value);
    setSitting(sittingValue);
    
  };

  const olevelIncomplete = (obj) => Object.values(obj).some(value => value === '');
  useEffect(() => {
    const validateForm = () => {
      const newMissingInfo = []
      if (!utme_score) newMissingInfo.push('UTME');
      if (postUtme_required && !postUtme_score) newMissingInfo.push('Post-UTME');
      if (olevel_required && olevelIncomplete(formData.olevelResults)) newMissingInfo.push('O-level result');
      if (sitting_required && !sitting) newMissingInfo.push('O-level sittings');
  
      setMissingInfo(newMissingInfo);
      
    };
  
    validateForm();
  }, [utme_score, postUtme_score, formData.olevelResults, postUtme_required, olevel_required, sitting_required, sitting]);
  
  
  
  
  
  const handleSubmit = async () => {
    setisButtonClicked(true)
    setLoading(true);
    setError(''); // Reset error before fetch
    if(missingInfo.length ===0){
      
      try {
        // Construct query parameters for the recommendation
        const queryParams = new URLSearchParams({
          course_name: selectedCourse || courses[0], // Use the selected course or the first course if none is selected
          utme_score: utme_score,
          post_utme_score: postUtme_score,
          no_of_sitting: sitting,
          grades: [
            formData.olevelResults.mathematics,
            formData.olevelResults.english,
            formData.olevelResults.subject1,
            formData.olevelResults.subject2,
            formData.olevelResults.subject3,
          ],
          university_name: university, // Use the selected university
          
        }).toString();
        formData.olevelResults.subject1;
  
        const response = await fetch(
          `${BASE_URL}/evaluations/recommendations?${queryParams}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
  
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
  
        const result = await response.json();
        setData(result); // Store the fetched data in state
      } catch (error) {
        console.log(error)
        setError('Something went wrong, please try again.'); // Set error message on failure
      } finally {
        setLoading(false); // Stop loading when the fetch is complete
      }
    }else {
      setMissingInfoError(missingInfo.join(', '));
      return;
    }
    
  };

  return (
    <>
      <div className='text-center my-8 px-2'>
        <h1 className='text-4xl font-bold text-gray-800 mb-4'>
          Calculate Your Aggregate Score
        </h1>
        <p className='text-lg text-gray-600'>
          Easily calculate your university admission aggregate score using your
          JAMB, WAEC, and Post-UTME results. <br /> Enter your details below to
          get started.
        </p>
      </div>

      <div className='form-wrap'>
          <div className='university-select'>
            <select onChange={updateUniversity} value={university} className='px-2'>
              <option value=''>Select University</option>
              {universities.length > 0 ? (
                universities.map((uni, index) => (
                  <option key={index} value={uni}>
                    {uni}
                  </option>
                ))
              ) : (
                <option disabled>Loading universities...</option>
              )}
            </select>
          </div>
        {university && <div className='course-score-input'>
          <div className='course-select mt-[20px]'>
              <select onChange={updateCourse} value={selectedCourse} className='px-2'>
                <option value=''>Select Course</option>
                {courses.length > 0 ? (
                  courses.map((course, index) => (
                    <option key={index} value={course}>
                      {course}
                    </option>
                  ))
                ) : (
                  <option disabled>Loading courses...</option>
                )}
              </select>
            </div>
          <div className='scores'>
            <div className='utme-postutme-input'>
              <label>
                UTME Score
                <br />
                <input
                  className='p-2'
                  type='number'
                  min='0'
                  max='400'
                  onChange={updateUtme_score}
                  onBlur={handleBlur} // Validate on blur
                  value={utme_score} // Controlled input, which will now be a string or empty
                />
                {utmeError && <p style={{ color: 'red' }}>{utmeError}</p>}{' '}
                {/* Display error message */}
              </label>
              { postUtme_required &&
              <label>
                Post UTME Score
                <br />
                <input
                  className='p-2'
                  type='number'
                  min='0'
                  max={maxPostUtmeScore} // Limit max value to maxPostUtmeScore
                  onChange={updatePostUtme_score}
                  onBlur={handlePostUtmeBlur} // Validate on blur
                  value={postUtme_score || ''} // Controlled input
                />
                {postUtmeError && <p style={{ color: 'red' }}>{postUtmeError}</p>}
              </label>}
            </div>
            { olevel_required &&
            <div className='mt-[20px]'>
              <p className='my-[20px]'>Enter your Olevel</p>
              <div className='grid w-full grid-cols-1 olevel_wrapper lg:grid-cols-3 lg:col-gap-16 lg:gap-x-32 mb-4 '>
                <div>
                  <label className='block'>
                    <span className='text-gray-700'>Mathematics</span>
                    <select
                      name='mathematics'
                      value={formData.olevelResults.mathematics}
                      onChange={handleChange}
                      className='block w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-200'
                    >
                      <option value='' disabled>Select Grade</option>
                      {grades.map((grade) => (
                        <option key={grade} value={grade}>
                          {grade}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
                <div>
                  <label className='block'>
                    <span className='text-gray-700'>English</span>
                    <select
                      name='english'
                      value={formData.olevelResults.english}
                      onChange={handleChange}
                      className='block w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-200'
                    >
                      <option value='' disabled>Select Grade</option>
                      {grades.map((grade) => (
                        <option key={grade} value={grade}>
                          {grade}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
                {/* Additional subjects follow the same structure */}
                <div>
                  <label className='block'>
                    <span className='text-gray-700'>Subject 1</span>
                    <select
                      name='subject1'
                      value={formData.olevelResults.subject1}
                      onChange={handleChange}
                      className='block w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-200'
                    >
                      <option value='' disabled>Select Grade</option>
                      {grades.map((grade) => (
                        <option key={grade} value={grade}>
                          {grade}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
                <div>
                  <label className='block'>
                    <span className='text-gray-700'>Subject 2</span>
                    <select
                      name='subject2'
                      value={formData.olevelResults.subject2}
                      onChange={handleChange}
                      className='block w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-200'
                    >
                      <option value='' disabled>Select Grade</option>
                      {grades.map((grade) => (
                        <option key={grade} value={grade}>
                          {grade}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
                <div>
                  <label className="block">
                    <span className="text-gray-700">Subject 3</span>
                    <select
                      name="subject3"
                      value={formData.olevelResults.subject3}
                      onChange={handleChange}
                      className="block w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-200"
                    >
                      <option value='' disabled>Select Grade</option>
                      {grades.map((grade) => (
                        <option key={grade} value={grade}>
                          {grade}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
                {/* Continue for other subjects */}
              </div>
            </div>}
            {sitting_required &&
              <label>
                  How many sittings(O-level)
                  <br />
                  <input
                    className="p-2"
                    type="number"
                    min={1}
                    onChange={updateSitting}
                    value={sitting} // Controlled input, which will now be a string or empty
                  />
                </label>
            }
          </div>
          {isButtonClicked && missingInfoError !== '' && <p className='text-red-700'>{missingInfoError} is missing</p>}
          <div className="submit-btn" >
            <button className="submit" onClick={handleSubmit}>
              Evaluate
            </button>
          </div>
        </div>}
        
      </div>

      <div className="evaluation">
        {!missingInfo && loading && <p>Loading...</p>}
        {error && <p>{error}</p>}
        {data && !loading && !error && (
          <div>
            <h2>Evaluation Results</h2>
            <div className="scroll-container">
              <table>
                <thead>
                  <tr>
                    <th>Course</th>
                    <th>Course Aggregate</th>
                    <th>Student's Aggregate</th>
                    <th>Faculty</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{data.course}</td>
                    <td>{data['course aggregate']}</td>
                    <td>{data["student's aggregate"]}</td>
                    <td>{data.faculty}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            {/* Conditionally render other recommended courses */}
            {Object.keys(data['other courses qualified for']).length > 0 ? (
              <div>
                <h3>Other Courses Qualified For:</h3>
                <div className='scroll-container'>
                  <table>
                    <thead>
                      <tr>
                        <th>Course</th>
                        <th>Aggregate</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.keys(data['other courses qualified for']).map(
                        (course) => (
                          <tr key={course}>
                            <td>{course}</td>
                            <td>
                              {data['other courses qualified for'][course]}
                            </td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <p>No other courses in the faculty qualified for</p>
            )}
          </div>
        )}
      </div>
    </>
  );
}

export default Aggregator;
