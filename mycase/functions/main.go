package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"golang.org/x/sync/semaphore"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
	"time"
)

//LIN – Lincoln Service Center (Nebraska Service Center)
//EAC – Eastern Adjudication Center (Vermont Service Center)
//IOE – USCIS Electronic Immigration System (ELIS)
//WAC – Western Adjudication Center (California Service Center)
//MSC – Missouri Service Center (National Benefits Center)
//NBC – National Benefits Center
//SRC – Southern Regional Center (Texas Service Center)
//YSC - Potomac Service Center
//

var CENTER_NAMES = []string{
	"LIN",
	"MSC",
	"SRC",
	"WAC",
	"EAC",
	"YSC",
	//"IOE",
}

var MONTHS = map[string]bool{
	"January":   true,
	"February":  true,
	"March":     true,
	"April":     true,
	"May":       true,
	"June":      true,
	"July":      true,
	"August":    true,
	"September": true,
	"October":   true,
	"November":  true,
	"December":  true,
}

var FORM_TYPES = []string{
	"I-129CW",
	"I-129F",
	"I-290B",
	"I-600A",
	"I-601A",
	"I-751A",
	"I-765V",
	"I-485J",
	"I-800A",
	"I-821D",
	"I-90",
	"I-102",
	"I-129",
	"I-130",
	"I-131",
	"I-140",
	"I-212",
	"I-360",
	"I-485",
	"I-526",
	"I-539",
	"I-600",
	"I-601",
	"I-612",
	"I-730",
	"I-751",
	"I-765",
	"I-800",
	"I-817",
	"I-821",
	"I-824",
	"I-829",
	"I-914",
	"I-918",
	"I-924",
	"I-929",
	"EOIR-29",
	"G-28",
}

type result struct {
	case_id string
	status  string
	form    string
	date    string
}

//var day_case_count_mutex sync.Mutex
//var day_case_count = make(map[int]int)

var case_status_store_mutex sync.Mutex
var case_status_store = make(map[string][]string)

var sem = semaphore.NewWeighted(1000)

func Split(r rune) bool {
	return r == ',' || r == ' '
}

func writeF(path string, content []byte) {
	err := os.WriteFile(path, content, 0666)
	if err != nil {
		fmt.Println("Write error! ", err.Error())
	}
}

func get(form url.Values, retry int) result {
	case_id := form.Get("appReceiptNum")
	if retry > 10 {
		return result{case_id, "try_faild", "NA", "NA"}
	}

	sem.Acquire(context.Background(), 1)
	res, err1 := http.PostForm("https://egov.uscis.gov/casestatus/mycasestatus.do", form)
	sem.Release(1)

	defer func() {
		if err1 == nil {
			res.Body.Close()
		}
	}()
	if err1 != nil {
		//fmt.Println("error 1! " + err1.Error())
		//fmt.Printf("Retry %d %s\n", retry+1, form)
		return get(form, retry+1)
	}

	doc, err2 := goquery.NewDocumentFromReader(res.Body)
	if err2 != nil {
		//fmt.Println("error 2! " + err2.Error())
		//fmt.Printf("Retry %d %s\n", retry+1, form)
		return get(form, retry+1)
	}

	body := doc.Find(".rows").First()
	status_h := body.Find("h1").Text()
	status_p := body.Find("p").Text()
	status_p_s := strings.FieldsFunc(status_p, Split)
	date_x := ""
	form_x := ""
	for i, w := range status_p_s {
		if MONTHS[w] {
			date_x = status_p_s[i] + " " + status_p_s[i+1] + ", " + status_p_s[i+2]
		} else if w == "Form" {
			form_x = status_p_s[i+1]
			break
		}
	}

	if status_h != "" {
		return result{case_id, status_h, form_x, date_x}
	} else {
		return result{case_id, "invalid_num", "NA", "NA"}
	}
}

func buildURL(center string, two_digit_yr int, day int, code int, case_serial_numbers int, format string) url.Values {
	if format == "sc" {
		res := url.Values{"appReceiptNum": {fmt.Sprintf("%s%d%03d%d%04d", center, two_digit_yr, day, code, case_serial_numbers)}}
		return res
	} else {
		res := url.Values{"appReceiptNum": {fmt.Sprintf("%s%d%d%03d%04d", center, two_digit_yr, code, day, case_serial_numbers)}}
		return res
	}
}

func crawlerAsync(center string, two_digit_yr int, day int, code int, case_serial_numbers int, format string, c chan result) {
	c <- crawler(center, two_digit_yr, day, code, case_serial_numbers, format)
}

func crawler(center string, two_digit_yr int, day int, code int, case_serial_numbers int, format string) result {
	url_x := buildURL(center, two_digit_yr, day, code, case_serial_numbers, format)
	res := get(url_x, 0)

	if res.status != "invalid_num" {
		//fmt.Printf("%s: %s %s %s\n", url_x.Get("appReceiptNum"), res.date, res.form, res.status)

		//case_status_store_mutex.Lock()
		//case_status_store[res.case_id] = []string{res.form, res.date, res.status}
		//case_status_store_mutex.Unlock()
	}
	return res
}

func getLastCaseNumber(center string, two_digit_yr int, day int, code int, format string) int {
	low := 1
	high := 1
	invalid_limit := 10
	i := 0
	for high < 10000 {
		for i = 0; i < invalid_limit; i++ {
			if crawler(center, two_digit_yr, day, code, high+i-1, format).status != "invalid_num" {
				high *= 2
				break
			}
		}
		if i == invalid_limit {
			break
		}
	}

	for low < high {
		mid := (low + high) / 2
		for i = 0; i < invalid_limit; i++ {
			if crawler(center, two_digit_yr, day, code, mid+i, format).status != "invalid_num" {
				low = mid + 1
				break
			}
		}

		if i == invalid_limit {
			high = mid
		}
	}
	return low - 1
}

func all(center string, two_digit_yr int, day int, code int, format string, report_c chan int) {
	defer func() { report_c <- 0 }()

	last := getLastCaseNumber(center, two_digit_yr, day, code, format)
	fmt.Printf("loading %s total of %d at day %d of format %s\n", center, last, day, format)

	c := make(chan result)
	for i := 0; i <= last; i++ {
		go crawlerAsync(center, two_digit_yr, day, code, i, format, c)
	}

	for i := 0; i <= last; i++ {
		cur := <-c
		if cur.status == "invalid_num" {
			continue
		}
		//fmt.Sprintf("%s:%s|%s|%s", cur.case_id, cur.form, cur.date, cur.status)

		case_status_store_mutex.Lock()
		case_status_store[cur.case_id] = []string{cur.form, cur.date, cur.status}
		case_status_store_mutex.Unlock()

	}

	//day_case_count_mutex.Lock()
	//day_case_count[day] = last
	//day_case_count_mutex.Unlock()

	fmt.Printf("Done %s total of %d at day %d of format %s\n", center, last, day, format)
}

func main() {
	fmt.Println(time.Now())
	center := "LIN"
	fiscal_year := 21
	format := "lb"

	year_days := 20

	dir, _ := os.Getwd()

	// Start the data retrieval
	if format == "lb" {
		report_c_lb := make(chan int)
		for day := 0; day <= year_days; day++ {
			go all(center, fiscal_year, day, 9, "lb", report_c_lb)
		}
		for i := 0; i <= year_days; i++ {
			<-report_c_lb
		}
	} else if format == "sc" {
		report_c_sc := make(chan int)
		for day := 0; day <= year_days; day++ {
			go all(center, fiscal_year, day, 5, "sc", report_c_sc)
		}
		for i := 0; i <= year_days; i++ {
			<-report_c_sc
		}
	} else if format == "ioe" {

	}

	// Save case status
	case_status_save_path := fmt.Sprintf("%s/saved_data/%s_%d_%s.json", dir, center, fiscal_year, format)
	b_status, _ := json.MarshalIndent(case_status_store, "", "  ")
	writeF(case_status_save_path, b_status)

	//total := 0
	//for _, e := range day_case_count {
	//	total += e
	//
	//}
	//fmt.Println("Total:", total)
	fmt.Println(time.Now())
}
