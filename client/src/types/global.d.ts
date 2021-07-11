interface KemonoAPI {
  errors: Map<string, string>,
  favorites: KemonoAPI.Favorites,
  posts: KemonoAPI.Posts
  api: KemonoAPI.API
}

namespace KemonoAPI {

  interface Post {
    id: string
    service: string
    title: string
    user: string
    added: string
    published: string
    attachments: string[]
    content: string
    edited: null
    embed: {}
    file: {}
    shared_file: boolean
  }

  interface Artist {
    id: string
    name: string
    service: string
    indexed: string
    updated: string
  }
  
  interface Favorites {
    retrieveFavoriteArtists: () => Promise<string>,
    favoriteArtist: (service: string, id: string) => Promise<boolean>,
    unfavoriteArtist: (service: string, id: string) => Promise<boolean>,
    retrieveFavoritePosts: () => Promise<string>,
    favoritePost: (service: string, user: string, post_id: string) => Promise<boolean>,
    unfavoritePost: (service: string, user: string, post_id: string) => Promise<boolean>
  }

  namespace Favorites {
    interface Artist extends KemonoAPI.Artist {
      faved_seq: number
    }

    interface Post extends KemonoAPI.Post {
      faved_seq: number
    }
  }

  interface Posts {
    attemptFlag: (service: string, user: string, post_id: string) => Promise<boolean>
  }

  interface API {
    bans: () => Promise<API.BanItem[]>
    bannedArtist: (id:string, service:string) => Promise<API.BannedArtist>
  }

  namespace API {
    interface BanItem {
      id: string
      service: string
    }

    interface BannedArtist {
      name: string
    }
  }
}
