import aiohttp, asyncio, time, json, threading


url = "https://jsonplaceholder.typicode.com/posts/{}"
num_of_posts = 77
lock = threading.Lock()

# for appending necessary characters in to the file accordingly
num_of_posts_written = 0


async def main():
    start_time = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        await fetch_and_write_posts(session)

    end_time = time.perf_counter()
    print(f"Time taken: {end_time - start_time:.2f} seconds")


# fetch post from url according to the given post id
async def get_post(session, post_id):
    global num_of_posts_written
    
    try:
        response = await session.get(url.format(post_id))
        post = await response.json()

        with lock:
            with open('posts.json', 'a') as file:
                json.dump(post, file, indent=4)
                
                num_of_posts_written += 1

                if num_of_posts_written < num_of_posts:
                    file.write(',\n')
                else:
                    file.write('\n]')

    except aiohttp.ClientConnectorError as e:
        print(f"Error fetching post {post_id}: {e}")

# truncate file and set its initial state
# fetch posts simultaneously and write them in to the file
async def fetch_and_write_posts(session):
    with open('posts.json', 'a') as file:
        file.seek(0)
        file.truncate()
        file.write('[\n')

    await asyncio.gather(*(get_post(session, id) for id in range(1, num_of_posts + 1)))


if __name__ == "__main__":
    asyncio.run(main())