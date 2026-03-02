import { TestBed } from '@angular/core/testing';
import { WebserviceService } from './webservice.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('WebserviceService', () => {

  let service: WebserviceService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [WebserviceService]
    });

    service = TestBed.inject(WebserviceService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should fetch courses from API', () => {

    const mockCourses = [
      { id: 1, name: 'Royal County Down', par: 72 },
      { id: 2, name: 'Royal Portrush', par: 72 }
    ];

    service.getCourses().subscribe(courses => {
      expect(courses.length).toBe(2);
      expect(courses[0].name).toBe('Royal County Down');
    });

    // 👇 IMPORTANT: Match the full URL
    const req = httpMock.expectOne(`${service['BASE_URL']}/courses`);

    expect(req.request.method).toBe('GET');

    req.flush(mockCourses);
  });

});
