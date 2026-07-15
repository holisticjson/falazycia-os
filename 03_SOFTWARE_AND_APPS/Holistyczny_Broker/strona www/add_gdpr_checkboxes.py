import glob
import re

checkbox_template = """
                        <!-- Zgoda RODO / GDPR (Quiet Luxury style) -->
                        <div class="flex items-start gap-3 my-6 text-xs text-slate-400">
                            <input type="checkbox" id="{id}" name="rodo_consent" required class="mt-1 w-4 h-4 rounded border-white/10 bg-brand-dark text-brand-gold focus:ring-0 focus:ring-offset-0 accent-brand-gold cursor-pointer">
                            <label for="{id}" class="leading-relaxed cursor-pointer select-none">
                                Wyrażam zgodę na przetwarzanie moich danych osobowych przez REVOLTO GROUP Sp. z o.o. w celu kontaktu handlowego, dystrybucji ofert Off-Market oraz realizacji usług zgodnie z <a href="polityka-prywatnosci.html" target="_blank" class="text-brand-gold hover:underline">Polityką Prywatności</a> oraz <a href="regulamin.html" target="_blank" class="text-brand-gold hover:underline">Regulaminem</a>.
                            </label>
                        </div>
"""

for filepath in glob.glob("*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "rodo_consent" in content or "Wyrażam zgodę na przetwarzanie" in content:
        print(f"File {filepath} already has GDPR checkbox or text. Skipping.")
        continue
    
    # Let's find all forms in the content
    # We can use a pattern to replace submit buttons inside forms with checkbox + submit button
    # Let's search for <button type="submit" ... or <button ... type="submit" ...
    
    # We find forms first:
    forms = list(re.finditer(r'(<form.*?</form>)', content, re.DOTALL | re.IGNORECASE))
    if not forms:
        continue
        
    print(f"Processing {filepath}...")
    new_content = content
    offset = 0
    
    for idx, match in enumerate(forms):
        form_text = match.group(1)
        form_start = match.start() + offset
        form_end = match.end() + offset
        
        # Unique ID for checkboxes on this page
        checkbox_id = f"rodo_consent_{idx}"
        
        # Let's find the submit button inside this form text
        # Usually it is <button type="submit" or <button class="... " type="submit" or similar
        button_match = re.search(r'(<button[^>]*?type=["\']submit["\'][^>]*?>)', form_text, re.IGNORECASE)
        if not button_match:
            # Fallback if type="submit" is at the end or button tag without type
            button_match = re.search(r'(<button[^>]*?class=["\'][^"\']*?submit[^"\']*?["\'][^>]*?>)', form_text, re.IGNORECASE)
            
        if button_match:
            btn_tag = button_match.group(1)
            btn_pos = form_text.find(btn_tag)
            
            # Insert checkbox before the submit button
            checkbox_html = checkbox_template.format(id=checkbox_id)
            modified_form_text = form_text[:btn_pos] + checkbox_html + form_text[btn_pos:]
            
            # Replace in new_content
            new_content = new_content[:form_start] + modified_form_text + new_content[form_end:]
            offset += len(modified_form_text) - len(form_text)
            print(f"  Added checkbox {checkbox_id} inside form {idx}")
        else:
            print(f"  Could not find submit button inside form {idx} of {filepath}")
            
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Saved {filepath}")
