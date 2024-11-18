import re
import argparse

'''
Простой скрипт цель которого найти потенциально уязвимые паттерны к DOM XSS. Для поиска используются регулярные выражения.
Ложно-позитивные сработки не обрабатываются.
'''

pattern_source = re.compile(r'(location.search|location.host|location.hostname|location.href|location.pathname|location.search|location.protocol|location.assign|location.replace|open|element.srcdoc|XMLHttpRequest.open.|location.hash|document.URL|document.documentURI|document.URLUnencoded|document.baseURI|document.referrer|window.name|history.pushState|history.replaceState|localStorage|sessionStorage|IndexedDB|(mozIndexedDB|webkitIndexedDB|msIndexedDB)|Database)', re.IGNORECASE | re.MULTILINE)
pattern_sink = re.compile(r'(WebSocket.|document.write|document.evaluate|setAttribute|document.domain|document.cookie|innerHTML|outerHTML|insertAdjacentHTML|onevent|.src|window.location|postMessage|setRequestHeader.|ExecuteSql.|eval|evaluate|execCommand|execScript|setTimeout|setInterval)', re.IGNORECASE | re.MULTILINE)

def find_pattern_in_html(file_path, pattern) -> str:
    # Compile the regex pattern once for efficiency
    matches = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                # Remove any leading/trailing whitespace
                cleaned_line = line.strip()
                
                # Find all matches in the line
                match_objects = pattern.finditer(cleaned_line)
                
                for match_object in match_objects:
                    start_pos = match_object.start()
                    end_pos = match_object.end()
                    
                    # Extract the matched text
                    matched_text = cleaned_line[start_pos:end_pos]
                    
                    # Add the match details to our list
                    matches.append({
                        'line_number': line_number,
                        'matched_text': matched_text,
                    })
        
        return matches
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def print_results(type, name_check) -> None:
    print(f"Start finding: {name_check}")
    if not type:
        print("No matches found.")
        return None
    
    print(f"Found {len(type)} matches:")
    for result in type:
        print(f"[+] Line {result['line_number']}. Matched pattern: '{result['matched_text']}'")

def main():
    parser = argparse.ArgumentParser(description="Simple script that find pattern in HTML content using regex. Usage: $findDOMXSS.py /path/to/page.html")
    parser.add_argument("html_content", nargs='*', help="- HTML content to analyze")
    args = parser.parse_args()

    if args.html_content:
        html_content = '\n'.join(args.html_content)
        print(html_content)
    elif not html_content.strip():
        print("No HTML content provided.")
    
    find_sources = find_pattern_in_html(html_content, pattern_source)
    print_results(find_sources, 'SOURCES')

    find_sinks = find_pattern_in_html(html_content, pattern_sink)
    print_results(find_sinks, 'SINKS')

if __name__ == "__main__":
    main()