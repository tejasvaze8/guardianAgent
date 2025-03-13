## Inspiration

We were inspired by Co-pilot AI, which supports coders during development. We aimed to create a plug-in that works with the data encountered in your web browser, providing insights for writing and general learning. Whether crafting an email, research paper, or documentation, our tool assists you as you write. For learning, it offers visual support by generating images or providing example data to help work through solutions. As students, we believed having an agent by your side would enhance your learning experience beyond just the code you write.

Devpost Link: [Guardian Agent](https://devpost.com/software/guardian-agent-sluxp6)

## What it does

The plug-in leverages Bedrock to provide multiple LLMs. When you highlight text, Guardian displays useful information from the LLMs to guide you through your work. Websites you encounter during research are stored in Convex, which is later used to provide better insights based on your browsing history. During the learning process, you can also generate images based on your needs, such as flowcharts and diagrams, to aid in understanding complex concepts.

## How we built it

We used AWS Bedrock to gather information from different LLMs and Convex to store and fetch data when an insight can be derived. AWS's Stable Diffusion enables image generation based on specific queries. We employed Launch Darkly to enable different LLMs based on region, ensuring outputs are tailored to specific users. Integrating these features into a Chrome extension, we created an all-purpose tool for any workspace in the browser.

## Challenges we ran into

We faced a learning curve with some of the new software we had to use. After testing with Bedrock and Convex, we figured out how to implement the tools in the Chrome plug-in and eventually integrate everything.

## Accomplishments that we're proud of

We successfully created a seamless tool that integrates various AI technologies to enhance productivity and learning. Overcoming the initial learning curve with new technologies was a significant achievement.

## What we learned

We gained a deep understanding of integrating multiple AI tools and technologies into a single cohesive product. We also learned the importance of user-centric design in developing tools that cater to diverse user needs.

## What's next for Guardian Agent

We plan to expand the capabilities of Guardian Agent by adding more features, improving user experience, and integrating additional AI models. We aim to make it an indispensable tool for anyone looking to enhance their productivity and learning in their browser workspace.
