using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

namespace TextFilter
{
    class Program
    {
        static string dictionaryFile = "stopwords.txt";
        static Dictionary<string, bool> stopWords = new Dictionary<string, bool>();
        
        public static string RemoveHTMLTags(string source) {
            return Regex.Replace(source, "<.*?>", string.Empty);
        }

        public static void ReadStopWords() {
            string[] lines = System.IO.File.ReadAllLines(dictionaryFile);
            foreach (string line in lines) {
                stopWords.Add(line, true);
            }
        }

        public static string RemoveJunkCharacters(string source) {
            string removedJunkChars = Regex.Replace(source, @"\b\d\b", string.Empty);
            removedJunkChars = Regex.Replace(removedJunkChars, "[^a-zA-Z0-9 .:_]", string.Empty);
            removedJunkChars = Regex.Replace(removedJunkChars, @"^\s+", string.Empty);
            return Regex.Replace(removedJunkChars, @"RawTextenglishText_\d+_\d+", string.Empty);
        }

        public static string[] SplitWords(string source) {
            return Regex.Split(source, "[^a-zA-Z0-9]+");
        }

        static void Main(string[] args) {
            ReadStopWords();
            Dictionary<string, int> dict = new Dictionary<string, int>();

            string[] lines = System.IO.File.ReadAllLines(args[0]);
            
            List<string> outNoStopWord = new List<string>();
            List<string> outNoHTML = new List<string>();
            foreach (string line in lines) {
                string cleanedLine = RemoveHTMLTags(line);
                cleanedLine = RemoveJunkCharacters(cleanedLine);

                if (cleanedLine.Length > 0) {
                    outNoHTML.Add(cleanedLine);
                }

                string newLine = "";
                foreach (string substring in SplitWords(cleanedLine)) {
                    if (substring.Length > 0) {
                        if (!stopWords.ContainsKey(substring.ToLower())) {
                            newLine = newLine + substring + " ";

                            if (!dict.ContainsKey(substring.ToLower())) {
                                dict.Add(substring.ToLower(), 1);
                            }
                            else {
                                dict[substring.ToLower()]++;
                            }
                        }
                    }
                }

                if (newLine.Length > 0) {
                    outNoStopWord.Add(newLine);
                }
            }
            System.IO.File.WriteAllLines(args[0] + ".noHTML", outNoHTML.ToArray());
            System.IO.File.WriteAllLines(args[0] + ".noStopWord", outNoStopWord.ToArray());

            // sort by value
            double sumWords = dict.Skip(1).Sum(v => v.Value);
            List<string> freq = new List<string>();
            foreach (KeyValuePair<string, int> item in dict.OrderByDescending(key => key.Value)) {
                freq.Add(String.Format("{0}, {1}", item.Key, 1.0 * item.Value / sumWords));
            }
            System.IO.File.WriteAllLines(args[0] + ".keyword", freq.ToArray());
        }
    }
}